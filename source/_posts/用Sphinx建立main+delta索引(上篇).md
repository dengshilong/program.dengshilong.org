title: 用Sphinx建立main+delta索引(上篇)
tags:
  - delta
  - main
  - Sphinx
  - Sphinx-for-chinese
  - 增量索引
id: 686
categories:
  - 搜索引擎
date: 2014-04-14 13:14:18
---

虽然只建立主索引就可以满足许多应用，但当数据非常多时，每次都重建索引是一件非常耗时的事情，而且每次重建都会浪费CPU，这也是极为不好的。考虑这样一种情况，在数据库中一共有1千万个文档，而每天只新增一万个文档，如果每次都要重建索引，则第一次重建时，是1001万个文档，第二次时是1002万个文档，这都非常耗时的。如果建好主索引后，只对这些新增的一万个数据建一个增量索引，之后把它合并到主索引中，所需的时间将缩短。所以建立main+delta索引是一个不错的选择。

这里依然以之前的博客搜索为例。为了便于做增量，我们需要记录每次抓取的时间，而为了持久保存这个时间，我们需要在数据中建立一个辅助表，建表语句如下
```
create table sphinx_helper(
        appid varchar(300) not null primary key,
        main_maxts datetime,
        main_tmp_maxts datetime,
        delta_maxts datetime,
        delta_tmp_maxts datetime
);
insert into sphinx_helper (appid) values ('blog_search');
```
在wp_posts表中, post_modified这个时间字段是随着每次文章的更新而自动变化的，所以可以使用它来做增量。主要思路就是用一个值来保存上次增量索引的时间，当需要再做增量索引时，则只需索引从这个保存的时间到现在这段时间里的数据。在sphinx_helper中，这个值用main_maxts来标示。对于主索引，写成配置文件如下，
```
source base{
        type = mysql
        sql_host = localhost
        sql_user = root
        sql_pass = 123456
        sql_db = blog
        sql_port = 3306
}
source srcmain : base{
        sql_query_pre = SET NAMES utf8
        sql_query_pre = SET SESSION query_cache_type=OFF
        sql_query_pre = UPDATE sphinx_helper SET main_tmp_maxts=NOW() WHERE appid='blog_search';
        sql_query = \
                SELECT ID, post_title, post_content, UNIX_TIMESTAMP(post_modified) AS post_modified FROM wp_posts WHERE \
                        post_status='publish' AND post_modified < (SELECT main_tmp_maxts FROM sphinx_helper WHERE appid='blog_search');
        sql_query_post_index = UPDATE sphinx_helper SET main_maxts=main_tmp_maxts WHERE appid='blog_search';
        sql_attr_timestamp = post_modified
        sql_field_string = post_title

}
```
以上就是主索引的配置，之所以需要将NOW()得到的时间保存到数据库中，之后在sql_query_post_index中取出来用，是因为sql_query_post_index和sql_query不是用一个数据连接。而之所以在sql_query_post_index里才更新main_maxts，是为了保证只有在索引成功建立后才更新这个值。而对于增量索引的配置，则如下：
```
source srcdelta : srcmain {
        sql_query_pre = SET NAMES utf8
        sql_query_pre = SET SESSION query_cache_type=OFF
        sql_query_pre = SET @maxtsdelta:=NOW();
        sql_query_pre = UPDATE sphinx_helper SET delta_tmp_maxts=@maxtsdelta WHERE appid='blog_search';
        sql_query = SELECT ID, post_title, post_content, UNIX_TIMESTAMP(post_modified) AS post_modified FROM wp_posts WHERE \
                post_status='publish' AND post_modified >= (SELECT main_maxts FROM sphinx_helper WHERE appid='blog_search')\
                AND post_modified < @maxtsdelta;
        sql_query_post_index = UPDATE sphinx_helper SET delta_maxts=delta_tmp_maxts WHERE appid='blog_search';
}
```
在sql_query中可以看到，每次增量索引的数据都是在[max_maxts, NOW()]之间，而只在sql_query_post_index中更新delta_maxts也是基于上述理由。剩下的配置如下：
```
index main {
        source = srcmain
        path = /home/long/sphinxforchinese/blog_search/var/data/main
        docinfo = extern
        charset_type = utf-8
        chinese_dictionary = /home/long/sphinxforchinese/blog_search/etc/xdict
}
index delta : main {
        source = srcdelta
        path = /home/long/sphinxforchinese/blog_search/var/data/delta
}

index dist_blog_search {
        type = distributed
        local = main
        local = delta
        agent_connect_timeout = 1000
        agent_query_timeout = 3000
}
```
这里我们多了一个dist_blog_search，它是结合main和delta的搜索结果，在客户端中搜索时，我们使用dist_blog_search这个索引的结果。剩下的配置与只有主索引时相同，这里就不累述了。

写好配置文件后，还需要有一个步骤。因为我们的策略是每隔一段时间将增量索引与主索引合并，当合并之后，我们需要更新main_maxts这个值。如果我们是每个60秒做一次增量索引，这需要写一个shell脚本，脚本如下：
```
#!/bin/bash
baseDir=/home/long/sphinxforchinese/blog_search
conf=$baseDir/etc/main_delta.conf
binDir=$baseDir/bin
cd $binDir
while [ true ]
do
        ./indexer -c $conf --rotate --merge main delta
        if [ "$?" -eq "0" ]; then
                cat $baseDir/script/post_merge.sql | mysql -u root --password=123456 blog
                ./indexer -c $conf --rotate delta
        fi
        sleep 60
done
```
先执行
```
 ./indexer -c $conf --rotate --merge main delta
```
这句是将主索引和增量索引合并，当合并成功时，则需要到数据库中修改main_maxts这个值，这个句子在post_merge.sql中，post_merge.sql的内容如下：
```
UPDATE sphinx_helper SET main_maxts=delta_maxts\
        WHERE appid='blog_search';
```
之后进行增量抓取
```
./indexer -c $conf --rotate delta
```
这里说说--rotate这个选项，这个选项非常有用。在主索引和增量索引合并时，indexer程序会将这两个索引合并成一个索引，当合并成功后，程序会发送一个SIGHUP信号给searchd，之后searchd就好去加载这个新的索引。

到这里，一个main+delta的索引就完成了。

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
<div></div>
<div>这里依然以之前的博客搜索为例。为了便于做增量，我们需要记录每次抓取的时间，而为了持久保存这个时间，我们需要在数据中建立一个辅助表，建表语句如下</div>
<div>
<div>create table sphinx_helper(</div>
<div>        appid varchar(300) not null primary key,</div>
<div>        main_maxts datetime,</div>
<div>        main_tmp_maxts datetime,</div>
<div>        delta_maxts datetime,</div>
<div>        delta_tmp_maxts datetime</div>
<div>);</div>
<div>insert into sphinx_helper (appid) values ('blog_search');</div>
<div>在wp_posts表中, post_modified这个时间字段是随着每次文章的更新而自动变化的，所以可以使用它来做增量。主要思路就是用一个值来保存上次增量索引的时间，当需要再做增量索引时，则只需索引从这个保存的时间到现在这段时间里的数据。在sphinx_helper中，这个值用main_maxts来标示。对于主索引，写成配置文件如下，</div>
<div>
<div>source base{</div>
<div>        type = mysql</div>
<div>        sql_host = localhost</div>
<div>        sql_user = root</div>
<div>        sql_pass = 123456</div>
<div>        sql_db = blog</div>
<div>        sql_port = 3306</div>
<div>}</div>
<div>source srcmain : base{</div>
<div>        sql_query_pre = SET NAMES utf8</div>
<div>        sql_query_pre = SET SESSION query_cache_type=OFF</div>
<div>        sql_query_pre = UPDATE sphinx_helper SET main_tmp_maxts=NOW() WHERE appid='blog_search';</div>
<div>        sql_query = \</div>
<div>                SELECT ID, post_title, post_content, UNIX_TIMESTAMP(post_modified) AS post_modified FROM wp_posts WHERE \</div>
<div>                        post_status='publish' AND post_modified < (SELECT main_tmp_maxts FROM sphinx_helper WHERE appid='blog_search');</div>
<div>        sql_query_post_index = UPDATE sphinx_helper SET main_maxts=main_tmp_maxts WHERE appid='blog_search';</div>
<div>        sql_attr_timestamp = post_modified</div>
<div>        sql_field_string = post_title</div>
<div></div>
<div>}</div>
<div></div>
<div>以上就是主索引的配置，之所以需要将NOW()得到的时间保存到数据库中，之后在sql_query_post_index中取出来用，是因为sql_query_post_index和sql_query不是用一个数据连接。而之所以在sql_query_post_index里才更新main_maxts，是为了保证只有在索引成功建立后才更新这个值。而对于增量索引的配置，则如下：</div>
<div></div>
<div>source srcdelta : srcmain {</div>
<div>        sql_query_pre = SET NAMES utf8</div>
<div>        sql_query_pre = SET SESSION query_cache_type=OFF</div>
<div>        sql_query_pre = SET @maxtsdelta:=NOW();</div>
<div>        sql_query_pre = UPDATE sphinx_helper SET delta_tmp_maxts=@maxtsdelta WHERE appid='blog_search';</div>
<div>        sql_query = SELECT ID, post_title, post_content, UNIX_TIMESTAMP(post_modified) AS post_modified FROM wp_posts WHERE \</div>
<div>                post_status='publish' AND post_modified >= (SELECT main_maxts FROM sphinx_helper WHERE appid='blog_search')\</div>
<div>                AND post_modified < @maxtsdelta;</div>
<div>        sql_query_post_index = UPDATE sphinx_helper SET delta_maxts=delta_tmp_maxts WHERE appid='blog_search';</div>
<div>}</div>
<div>在sql_query中可以看到，每次增量索引的数据都是在[max_maxts, NOW()]之间，而只在sql_query_post_index中更新delta_maxts也是基于上述理由。剩下的配置如下：</div>
<div>index main {</div>
<div>        source = srcmain</div>
<div>        path = /home/long/sphinxforchinese/blog_search/var/data/main</div>
<div>        docinfo = extern</div>
<div>        charset_type = utf-8</div>
<div>        chinese_dictionary = /home/long/sphinxforchinese/blog_search/etc/xdict</div>
<div>}</div>
<div>index delta : main {</div>
<div>        source = srcdelta</div>
<div>        path = /home/long/sphinxforchinese/blog_search/var/data/delta</div>
<div>}</div>
<div>
<div>index dist_blog_search {</div>
<div>        type = distributed</div>
<div>        local = main</div>
<div>        local = delta</div>
<div>        agent_connect_timeout = 1000</div>
<div>        agent_query_timeout = 3000</div>
<div>}</div>
</div>
<div>这里我们多了一个dist_blog_search，它是结合main和delta的搜索结果，在客户端中搜索时，我们使用dist_blog_search这个索引的结果。剩下的配置与只有主索引时相同，这里就不累述了。</div>
</div>
<div>
<div></div>
<div>写好配置文件后，还需要有一个步骤。因为我们的策略是每隔一段时间将增量索引与主索引合并，当合并之后，我们需要更新main_maxts这个值。如果我们是每个60秒做一次增量索引，这需要写一个shell脚本，脚本如下：</div>
</div>
<div>
<div>#!/bin/bash</div>
<div>baseDir=/home/long/sphinxforchinese/blog_search</div>
<div>conf=$baseDir/etc/main_delta.conf</div>
<div>binDir=$baseDir/bin</div>
<div>cd $binDir</div>
<div>while [ true ]</div>
<div>do</div>
<div>        ./indexer -c $conf --rotate --merge main delta</div>
<div>        if [ "$?" -eq "0" ]; then</div>
<div>                cat $baseDir/script/post_merge.sql | mysql -u root --password=123456 blog</div>
<div>                ./indexer -c $conf --rotate delta</div>
<div>        fi</div>
<div>        sleep 60</div>
<div>done</div>
</div>
<div>先执行</div>
<div> ./indexer -c $conf --rotate --merge main delta</div>
<div>这句是将主索引和增量索引合并，当合并成功时，则需要到数据库中修改main_maxts这个值，这个句子在post_merge.sql中，post_merge.sql的内容如下：</div>
<div>
<div>UPDATE sphinx_helper SET main_maxts=delta_maxts\</div>
<div>        WHERE appid='blog_search';</div>
</div>
<div>之后进行增量抓取</div>
<div>./indexer -c $conf --rotate delta</div>
<div>这里说说--rotate这个选项，这个选项非常有用。在主索引和增量索引合并时，indexer程序会将这两个索引合并成一个索引，当合并成功后，程序会发送一个SIGHUP信号给searchd，之后searchd就好去加载这个新的索引。</div>
<div></div>
<div>到这里，一个main+delta的索引就完成了。</div>
<div></div>
<div></div>
<div></div>
</div>
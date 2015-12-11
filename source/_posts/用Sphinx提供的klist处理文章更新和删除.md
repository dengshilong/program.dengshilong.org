title: 用Sphinx提供的klist处理文章更新和删除
tags:
  - Klist
  - Klists
  - Sphinx
  - Sphinx-for-chinese
  - 删除
  - 更新
id: 691
categories:
  - 搜索引擎
date: 2014-04-14 13:18:16
---

在前面的介绍中，都没有处理更新和删除问题，这里有必要说说。在[关于sphinx引擎的一些想法](http://program.dengshilong.org/2014/04/11/关于sphinx引擎的一些想法/)中说过公司所用的引擎中，处理更新和删除的办法是在索引中增加一个属性来标志这条记录是否失效，每次做增量时，就要去主索引和增量索引中更改相应id的属性值，这确实可以解决问题。不过并不是一个很好的解决办法，Sphinx的作者也说过这种方法既麻烦又容易出错。既然有更新和删除这个需求，必然会提供解决的办法，这个办法就是kilst。所谓的klist，就是kill list,按照字面理解，就是删除列表。我们只需要在增量索引中保存一个id列表，搜索时，如果在主索引中搜到相关文档，而文档的id存在于增量索引的id列表中，则这个文档将被丢弃。

这里有一个需要注意的是，当文章被删除时，仅仅通过增量抓取，在增量索引中并不能知道主索引中哪一个文档被删除了，所以这就必须在表中文档被删除时，能够记录下被删除的id，这就需要用到触发器，也需要建立一个辅助表来保存这些id。辅助表的建立如下：
<div>create table sphinxklist(</div>
<div>        id integer not null,</div>
<div>        ts timestamp not null</div>
<div>);</div>
触发器的建立如下：
<div>DELIMITER //</div>
<div>CREATE TRIGGER sphinx_kill</div>
<div>AFTER DELETE ON wp_posts</div>
<div>FOR EACH ROW</div>
<div>BEGIN</div>
<div>        INSERT INTO sphinxklist VALUES (OLD.ID, NOW());</div>
<div>END</div>
<div>//</div>
有了这些准备工作后，我们就可以使用klist了，事实上在之前的配置文件的基础上，只需要修改一点点内容就好了。首先修改主索引
<div>source srcmain : base{</div>
<div>        sql_query_pre = SET NAMES utf8</div>
<div>        sql_query_pre = SET SESSION query_cache_type=OFF</div>
<div>        sql_query_pre = UPDATE sphinx_helper SET main_tmp_maxts=NOW() WHERE appid='blog_search';</div>
<div>        sql_query = \</div>
<div>                SELECT ID, post_title, post_content, UNIX_TIMESTAMP(post_modified) AS post_modified FROM wp_posts WHERE \</div>
<div>                        post_status='publish' AND post_modified < (SELECT main_tmp_maxts FROM sphinx_helper WHERE appid='blog_search');</div>
<div>        sql_query_post_index = UPDATE sphinx_helper SET main_maxts=main_tmp_maxts WHERE appid='blog_search';</div>
<div>        sql_query_post_index = DELETE FROM sphinxklist WHERE ts < (SELECT main_maxts FROM sphinx_helper WHERE appid='blog_search');</div>
<div>        sql_attr_timestamp = post_modified</div>
<div>        sql_field_string = post_title</div>
<div>}</div>
可以看到，相对于之前的配置，这里只添加了一行
sql_query_post_index = DELETE FROM sphinxklist WHERE ts < (SELECT main_maxts FROM sphinx_helper WHERE appid='blog_search');
添加这行是为了防止之前运行引擎时留下的id再次被使用。
之后修改临时索引：
<div>source srcdelta_temp : srcmain {</div>
<div>        sql_query_pre = SET NAMES utf8</div>
<div>        sql_query_pre = SET SESSION query_cache_type=OFF</div>
<div>        sql_query_pre = SET @maxtsdelta:=NOW();</div>
<div>        sql_query_pre = UPDATE sphinx_helper SET delta_tmp_maxts=@maxtsdelta WHERE appid='blog_search';</div>
<div>        sql_query = SELECT ID, post_title, post_content, UNIX_TIMESTAMP(post_modified) AS post_modified FROM wp_posts WHERE \</div>
<div>                post_status='publish' AND post_modified >= (SELECT main_maxts FROM sphinx_helper WHERE appid='blog_search')\</div>
<div>                AND post_modified < @maxtsdelta;</div>
<div>        sql_query_killlist = SELECT ID FROM wp_posts WHERE post_modified >= (SELECT main_maxts FROM sphinx_helper WHERE \</div>
<div>                appid='blog_search') AND post_modified < @maxtsdelta UNION SELECT id FROM sphinxklist;</div>
<div>        sql_query_post_index = UPDATE sphinx_helper SET delta_maxts=delta_tmp_maxts WHERE appid='blog_search';</div>
<div>}</div>
也只是添加了一行，也就是将这次抓取的id与sphinxlist中的id合并。
之后还需要修改Shell脚本
<div>#!/bin/bash</div>
<div>baseDir=/home/long/sphinxforchinese/blog_search</div>
<div>conf=$baseDir/etc/blog_search.conf</div>
<div>binDir=$baseDir/bin</div>
<div>cd $binDir</div>
<div>while [ true ]</div>
<div>do</div>
<div>        #./indexer -c $conf --merge-klists --rotate --merge delta deltaTemp</div>
<div>        ./indexer -c $conf  --merge-klists --rotate --merge delta delta_temp</div>
<div>        if [ "$?" -eq "0" ]; then</div>
<div>                cat $baseDir/script/post_merge.sql | mysql -u root --password=123456 blog</div>
<div>                ./indexer -c $conf --rotate delta_temp</div>
<div>        fi</div>
<div>        sleep 60</div>
<div>done</div>
这个脚本相对于原来的只增加了--merge-klists这个参数，这个参数的意义是，将delta_temp合并到delta时，并不会删除delta的klist,而是将delta_temp的klist和delta的klist合并，这正是我们想要的。经过这样的变化，一个可以处理更新和删除的main+delta索引就建好了。

感谢Sphinx团队，感谢Sphinx-for-chinese团队，给我们提供了一个这么好用的开源引擎。
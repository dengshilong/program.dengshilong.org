title: 用Sphinx建立main+delta索引(下篇)
tags:
  - Sphinx-for-chinese
  - 临时索引
  - 增量索引
id: 688
categories:
  - 搜索引擎
date: 2014-04-14 13:16:11
---

<div>在[上篇](http://program.dengshilong.org/2014/04/14/用sphinx建立maindelta索引上篇/)中，我们介绍了一种建立主索引和增量索引的方法，这种方法有一种不足之处就是会改变主索引，因为每次增量索引都会与主索引合并成新的主索引。为此，我们可以想出另一种解决的办法，每次只改变增量索引，这就需要另外再建立一个临时索引。</div>
<div></div>
<div>
<div>这里只需要改变少量地方，一个是增量索引，另外还需新增一个临时索引，具体配置如下：</div>
<div>
<div>source srcdelta : srcmain{</div>
<div>        sql_query_pre = SET NAMES utf8</div>
<div>        sql_query_pre = SET SESSION query_cache_type=OFF</div>
<div>        sql_query = SELECT ID, post_title, post_content, UNIX_TIMESTAMP(post_modified) AS post_modified FROM wp_posts WHERE \</div>
<div>                post_status='publish' limit 0;</div>
<div>        sql_query_post_index =</div>
<div>}</div>
<div>source srcdelta_temp : srcmain {</div>
<div>        sql_query_pre = SET NAMES utf8</div>
<div>        sql_query_pre = SET SESSION query_cache_type=OFF</div>
<div>        sql_query_pre = SET @maxtsdelta:=NOW();</div>
<div>        sql_query_pre = UPDATE sphinx_helper SET delta_tmp_maxts=@maxtsdelta WHERE appid='blog_search';</div>
<div>        sql_query = SELECT ID, post_title, post_content, UNIX_TIMESTAMP(post_modified) AS post_modified FROM wp_posts WHERE \</div>
<div>                post_status='publish' AND post_modified >= (SELECT main_maxts FROM sphinx_helper WHERE appid='blog_search')\</div>
<div>                AND post_modified < @maxtsdelta;</div>
<div>        sql_query_post_index = UPDATE sphinx_helper SET delta_maxts=delta_tmp_maxts WHERE appid='blog_search';</div>
<div>}</div>
<div>index delta_temp : main{</div>
<div>        source = srcdelta_temp</div>
<div>        path = /home/long/sphinxforchinese/blog_search/var/data/delta_temp</div>
<div>}</div>
</div>
<div>实际上，我们是先建立一个空的增量索引，之后临时索引中的数据慢慢合并到增量索引中。在这里，增量索引很像上篇中的主索引，而临时索引则像上篇中的增量索引。</div>
<div>此时我们需要修改dist_blog_search,即增加临时索引</div>
<div>
<div>
<div>index dist_blog_search {</div>
<div>    type = distributed</div>
<div>    local = main</div>
<div>    local = delta</div>
<div>    local = delta_temp</div>
<div>    agent_connect_timeout = 1000</div>
<div>    agent_query_timeout = 3000</div>
</div>
<div>}</div>
</div>
<div>此后还需改变Shell脚本的内容</div>
<div>
<div>#!/bin/bash</div>
<div>baseDir=/home/long/sphinxforchinese/blog_search</div>
<div>conf=$baseDir/etc/main_delta_temp.conf</div>
<div>binDir=$baseDir/bin</div>
<div>cd $binDir</div>
<div>while [ true ]</div>
<div>do</div>
<div>        ./indexer -c $conf  --rotate --merge delta delta_temp</div>
<div>        if [ "$?" -eq "0" ]; then</div>
<div>                cat $baseDir/script/post_merge.sql | mysql -u root --password=123456 blog</div>
<div>                ./indexer -c $conf --rotate delta_temp</div>
<div>        fi</div>
<div>        sleep 60</div>
<div>done</div>
</div>
<div>事实上，改变的内容还是很少的。经过这样的改变，我们就无需再改变主索引了。第一次建立主索引后，就一直保持不变，变化的是增量索引。</div>
</div>
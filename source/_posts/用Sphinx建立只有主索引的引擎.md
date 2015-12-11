title: 用Sphinx建立只有主索引的引擎
tags:
  - Sphinx
  - Sphinx-for-chinese
  - 主索引
  - 速度
id: 670
categories:
  - 搜索引擎
date: 2014-04-14 13:12:11
---

因为一直都对Wordpress自带的搜索功能略有微词，可是又不想去改它，想想自己的博客一天都没有一个人会访问，更不用说这个搜索功能了。因为现在学习使用Sphinx-for-chinese，拿博客的数据来练练手。

先从最简单的情况开始，以后再一步一步的完善功能，这样才符合学习的线路，从易到难，而不是一开始就给你一个很完善的模型，然后改改路径就好了。最简单的情况就是只有一个主索引，然后隔一段时间重建索引。得益于Sphinx的高效，建索引的速度非常快，在文档中说达到了10M/s, 按照一篇文章为4KB计算，一秒钟可以给250篇文章建索引了，对于博客来说，已经足够了。对于其它的应用，当数据不多时，只有一个主索引也是可以的。

这里只使用了wp_posts表中的数据，只是用了ID, post_title, post_content, post_modified四个字段，所以非常的简单，直接上配置文件
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
        sql_query = \
                SELECT ID, post_title, post_content, UNIX_TIMESTAMP(post_modified) AS post_modified FROM wp_posts WHERE \
                        post_status='publish' AND post_modified < NOW();
        sql_attr_timestamp = post_modified
        sql_field_string = post_title

}
index main {
        source = srcmain
        path = /home/long/sphinxforchinese/blog_search/var/data/main
        docinfo = extern
        charset_type = utf-8
        chinese_dictionary = /home/long/sphinxforchinese/blog_search/etc/xdict
}
indexer {
        mem_limit = 32M
}

searchd {
        listen = 9300
        log = /home/long/sphinxforchinese/blog_search/var/log/searchd.log
        query_log = /home/long/sphinxforchinese/var/log/query.log
        read_timeout = 5
        max_children = 30
        pid_file = /home/long/sphinxforchinese/var/log/searchd.pid
        max_matches = 1000
        seamless_rotate = 1
        preopen_indexes = 1
        unlink_old = 1
        workers = threads
        binlog_path = /home/long/sphinxforchinese/var/data
}
```
相关配置选项的意义可以查看示例，写的非常的详细。这里没有对post_content进行定义，因为只想对这个字段建索引，并不想保存它的原始内容，所以这里使用了默认行为，也就是只建索引。
建好索引，搜索跑步的相关文章，得到如下结果
1. document=41, weight=2661, post_title=跑步一周年, post_modified=Sun Apr 7 10:11:56 2013
2. document=286, weight=2660, post_title=跑步两周年, post_modified=Fri Jan 4 12:49:47 2013
3. document=537, weight=1642, post_title=写在广州马拉松之前, post_modified=Sat Nov 9 00:00:45 2013
4. document=39, weight=1632, post_title=看棒球英豪漫画, post_modified=Sun Apr 7 09:57:34 2013
5. document=2, weight=1626, post_title=关于我, post_modified=Fri Jun 14 19:49:08 2013
6. document=565, weight=1626, post_title=2013广州马拉松纪实, post_modified=Sun Nov 24 22:10:57 2013
7. document=43, weight=1617, post_title=三个月来的小结, post_modified=Sun Apr 7 10:10:22 2013
8. document=56, weight=1617, post_title=价值博客们, post_modified=Sun Apr 7 09:52:51 2013
9. document=205, weight=1617, post_title=2012扬州马拉松纪实, post_modified=Tue Apr 2 11:29:04 2013
10. document=5, weight=1602, post_title=2011年的阅读, post_modified=Tue May 29 11:19:49 2012
11. document=305, weight=1602, post_title=羽毛球心结, post_modified=Mon Apr 8 08:33:37 2013
12. document=40, weight=1574, post_title=通关manufactoria, post_modified=Sun Apr 7 10:01:06 2013
13. document=233, weight=1574, post_title=当了一回胃扩张, post_modified=Fri Jul 20 15:46:35 2012
搜索结果还行吧。

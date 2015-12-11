title: Solr索引升级
tags:
  - solr
  - 索引
id: 984
categories:
  - 搜索引擎
date: 2014-12-27 10:27:18
---

相信现在很多人还在用Solr1.4,因为Solr1.4许多时候还是满足需求了。可是总有一天会想升级，因为新版本中的一些功能和特性让使用Solr更加方便。而如果要从Solr1.4升级到Solr4.8,可以经过Solr1.4->Solr3.6->Solr4.0->Solr4.8这个步骤.

从Solr1.4->Solr3.6，去官网下载Solr3.6,使用需要升级的索引搭建起Solr引擎，执行curl 'http://localhost:8983/solr/update?optimize=true&maxSegments=1&waitFlush=false'即可

从Solr3.6->Solr4.0,去官网下载Solr4.0, 将lucene-core-4.0.jar拷贝到某一目录下，如：lib4.0/lucene-core-4.0.jar(注意，可能需要其它的包如：slf-api和log-back相关包，同样拷贝到lib4.0目录下), 之后执行java -cp "lib4.0/*" org.apache.lucene.index.IndexUpgrader -verbose index/, 这里 index目录存放着Solr3.6索引文件。

从Solr4.0->Solr4.8, 去官网下载Solr4.8,将lucene-core-4.8拷贝到某一目录下, 如：lib4.0/lucene-core-4.8.jar,之后执行../jdk1.7/bin/java -cp "lib4.8/*" org.apache.lucene.index.IndexUpgrader -delete-prior-commits -verbose index/，这里因为Solr4.8需要用到jdk1.7，所以执行java命令时，必须是jdk1.7。
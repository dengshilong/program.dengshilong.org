title: 在Intellij中启动ElasticSearch
date: 2016-04-03 21:03:21
tags: 
    - Elasticsearch
    - Intellij
categories:
    - 搜索引擎
---
有时候真的很郁闷，想要对Solr和Elasticsearch进行二次开发，结果在Eclipse和Intellij上，都不知道怎么启动，官网也没有说，只能上网找或者自己摸索。上网找也是很耗时间的，这些人就不能在官网上记一下吗？这里记下遇到的问题，目前使用Intellij进行Java开发，所以只纪录Intellij的情况。

## 下载源码
官网没有提供源码的下载，所以只好到github仓库上下载，尝试用`git clone -b 2.3 https://github.com/elastic/elasticsearch.git`, 但下载到的是2.3.1的，于是纠结要怎么样才能得到2.3.0的，最后求助于之前的搜索同事，知道在[https://github.com/elastic/elasticsearch/releases](https://github.com/elastic/elasticsearch/releases)里可以下载。

## 主程序入口
查看elasticsearch脚本，发现程序入口是org.elasticsearch.bootstrap.ElasticSearch

## path.home is not configured

参考[elasticsearch2.0源码在开发环境eclipse中启动的问题及解决方案](http://blog.csdn.net/jianjun200607/article/details/49821813#reply)

查看执行./elasticsearch脚本启动时添加的参数，设置VM options为
```
-Xms256m -Xmx1g -Djava.awt.headless=true -XX:+UseParNewGC -XX:+UseConcMarkSweepGC -XX:CMSInitiatingOccupancyFraction=75 -XX:+UseCMSInitiatingOccupancyOnly -XX:+HeapDumpOnOutOfMemoryError -XX:+DisableExplicitGC -Dfile.encoding=UTF-8 -Djna.nosys=true -Des.path.home=/Users/long/elasticsearch
```
其中主要是设置es.path.home,目录位置并没有限制。设置Program arguments为start

## "java.lang.IllegalStateException" jar hell!

参考[https://github.com/elastic/elasticsearch/pull/13465](https://github.com/elastic/elasticsearch/pull/13465)

```
I stripped the SDK classpath in IntelliJ down to the default sun.boot.class.path and I am not seeing jar hell failures anymore. Specifically:

jre/lib/charsets.jar
jre/lib/jce.jar
jre/lib/jfr.jar
jre/lib/jsse.jar
jre/lib/resources.jar
jre/lib/rt.jar
```
到这里才想起来Intellij在导入jdk时，将许多的jar包加入到Classpath中了，进入File->Other Settings->Default Project Structure,修改jdk的Classpath为
```
jre/lib/charsets.jar
jre/lib/jce.jar
jre/lib/jfr.jar
jre/lib/jsse.jar
jre/lib/resources.jar
jre/lib/rt.jar
```
## 提示找不到config目录
在/Users/long/program/java/elasticsearch-2.3.0/core目录下新建config目录，将官方发布的Elasticsearch可执行包里的config目录拷贝到这里。

之后启动org.elasticsearch.bootstrap.Elasticsearch, 成功。

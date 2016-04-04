title: Solr从MySQL导数据
date: 2016-04-04 14:07:18
tags: 
    - Solr
categories:
    - 搜索引擎
---
本来打算用Solr来搭建搜索服务，而公司的数据放在MySQL数据里，于是在文档里找到DataImportHandler,参考[https://wiki.apache.org/solr/DataImportHandler](https://wiki.apache.org/solr/DataImportHandler), 这里以导入Wordpress数据为例
## 在conf目录下新建data-config.xml

data-config.xml的内容为
```
<dataConfig>
  <dataSource type="JdbcDataSource" 
              driver="com.mysql.jdbc.Driver"
              url="jdbc:mysql://localhost/blog" 
              user="blog" 
              password="12345678"/>
  <document>
    <entity name="post" pk="ID"
            query="select ID,post_title,post_content from wp_posts where post_status='publish'"
            deltaImportQuery="select ID,post_title,post_content from wp_posts where ID='${dih.delta.ID}'"
            deltaQuery="select ID from wp_posts where post_status='publish' and post_modified_gmt > '${dih.last_index_time}'">
      <field column="ID" name="id"/>
      <field column="post_title" name="title"/>
      <field column="post_content" name="content"/>
    </entity>
  </document>
</dataConfig>
```
## 配置schema.xml
```
 <field name="id" type="string" indexed="true" stored="true" required="true" multiValued="false" /> 
<field name="title" type="text_general" indexed="true" stored="true" required="true" multiValued="false" /> 
<field name="content" type="text_general" indexed="true" stored="true" required="true" multiValued="false" /> 
```
## 修改solrconfig.xml
在solrconfig.xml增加
`<lib dir="${solr.install.dir:../../../..}/dist/" regex="solr-dataimporthandler-.*\.jar" />`,这样就不会报solr.Dataimport Class not found error.
* 添加jdbc连接mysql

在server/lib里添加mysql-connector-java-5.1.38.jar，我这里下载到的是5.1.38,其它版本的也可以。

* 新建core.properties

在blog目录下新建core.properties文件，内容为
```
#Written by CorePropertiesLocator
#Wed Mar 23 10:55:00 UTC 2016
numShards=1
collection.configName=blog
#name=blog_shard1_replica1
shard=shard1
collection=blog
coreNodeName=core_node1
```
* 启动Solr

bin/solr start -s server/solr/blog启动Solr

## 执行全量索引
命令为`http://127.0.0.1:8983/solr/blog/dataimport?command=full-import`
## 执行增量索引
命令为`http://127.0.0.1:8983/solr/blog/dataimport?command=delta-import`


## 遇到的问题
* nohup: can't detach from console: Inappropriate ioctl for device

这个问题时在搭建SolrCloud时遇到的，在这里不妨说说。在启动zookeeper时，遇到这个问题，网上说时因为在tmux里启动的缘故，于是新开一个终端,启动zookeeper,这次正常启动。
* /Users/long/program/java/solr-5.5.0/solr/server/logs/solr.log: No such file or directory

执行命令`bin/solr start -s server/solr/blog`时出现这个错误，莫名奇妙的，我想依然是不能在tmux里执行shell, 于是新开一个终端再次执行，这次正常启动

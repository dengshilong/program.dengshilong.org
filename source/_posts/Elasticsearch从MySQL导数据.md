title: Elasticsearch从MySQL导数据
date: 2016-04-10 17:00:01
tags: Elasticsearch MySQL
categories: 搜索引擎
---
在Solr和Elasticsearch两个中权衡，最后还是选择了Elasticsearch。虽然之前有Solr开发经验，但是当看过Elasticsearch的配置后，还是投奔Elasticsearch,只能说Solr的配置太复杂了。

依然是要从MySQL中导数据，在[http://www.jianshu.com/p/05cff717563c](http://www.jianshu.com/p/05cff717563c)中看到一些解决方案。因为对Mysql的binlog并不了解，而搜索elasticsearch-river-jdbc时，只搜到了[elasticsearch-jdbc](https://github.com/jprante/elasticsearch-jdbc),于是决定使用它。

## 增量导入数据
决定使用elasticsearch-jdbc后,使用增量导MySQL数据时发现官方文档，写的不好，而且竟然连向数据库提交的查询语句都不输出日志，出现问题时很难找错。

在使用增量导数据时，一直找不到它导入时间的存储位置，于是只好看代码，发现statefile的配置很重要，于是将它加上。但还是发现需要做一次全量导入后，这个增量导入才有效。

于是修改README
```
There is a problem here, the first time you run the script, it can't select any data from table, it have two solutions here:

1. in another script, do full-import, later you can use the incremental script to select incremental data
2. define a statefile.json file before the first time you run the incremental script, set the lastexecutionstart to 0, so that you can select all the data from table.
```

今天发现，为何不在，开始时间设置为0，这样就可以做全亮导入了，于是提交了一个新的patch.
## 定时导数据
原计划是在crontab里添加定时执行任务, 所以没看elasticsearch-jdbc提供的schedule功能，但看到issue中有人提到，于是开始解决。最后发现schedule时没有重新加载statefile文件，于是提交了一个patch。这次也把向数据库提交的查询语句打印出来，方便找错。
## 结束语
无法删除数据确实是一个很严重的缺陷，看来还是要想办法从binlog里读取数据才行,先这样做吧，以后再优化。

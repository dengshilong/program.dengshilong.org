title: Elasticsearch从MySQL增量导数据
date: 2016-05-30 22:03:02
tags:
    - Elasticsearch
    - elasticsearch-jdbc
categories:
    - 搜索引擎
---
自从写了Elasticsearch从MySQL到数据，收到几位同学的来信，主要是问如何使用elasticsearch-jdbc进行增量数据导入，这里还是写写具体操作。这里以从Wordpress导数据为例。

## Elasticsearch准备

* 新建索引

curl -XPUT 'localhost:9200/article?pretty'

* 新建type

curl -XPUT 'localhost:9200/article/_mappings/blog' -d '@mapping.json'

mapping.json内容
```
{
    "_all": {
        "enabled" : true,
        "analyzer": "ik_max_word_syno",
        "search_analyzer": "ik_smart"
    },
    "properties": {
        "id": {
            "type": "string",
            "index": "not_analyzed",
            "include_in_all": false
        },
        "title": {
            "type": "string",
            "analyzer": "ik_max_word_syno",
            "search_analyzer": "ik_smart",
            "boost": 2
        },
        "content": {
            "type": "string",
            "analyzer": "ik_max_word_syno",
            "search_analyzer": "ik_smart"
        }
    }
}
```

分词配置可参看
[Elatcissearch中ik添加同义词](
http://program.dengshilong.org/2016/04/06/Elasticsearch%E4%B8%ADik%E6%B7%BB%E5%8A%A0%E5%90%8C%E4%B9%89%E8%AF%8D/)

* 查看mapping
curl -XGET 'localhost:9200/article/_mapping'

## elasticsearch-jdbc配置

到elasticsearch-jdbc的bin目录下，查看mysql-blog.sh文件, 内容如下
```
#!/bin/sh

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
bin=${DIR}/../bin
lib=${DIR}/../lib

echo '
{
    "type" : "jdbc",
    "jdbc" : {
        "url" : "jdbc:mysql://localhost:3306/blog",
        "statefile" : "statefile.json",
        "schedule" : "0 0-59 0-23 ? * *",
        "user" : "blog",
        "password" : "12345678",
        "sql" : [{
                "statement": "select id as _id, id, post_title as title, post_content as content from wp_posts where post_status = ? and post_modified > ? ",
                "parameter": ["publish", "$metrics.lastexecutionstart"]}
            ],
        "index" : "article",
        "type" : "blog",
         "metrics": {
            "enabled" : true
        },
        "elasticsearch" : {
             "cluster" : "elasticsearch",
             "host" : "localhost",
             "port" : 9300
        }
    }
}
' | java \
    -cp "${lib}/*" \
    -Dlog4j.configurationFile=${bin}/log4j2.xml \
    org.xbib.tools.Runner \
    org.xbib.tools.JDBCImporter
```
这里主要看两个配置, statefile和schedule,

其中statefile这个配置对于增量导数据一定不能少。因为只有配置了statefile，elasticsearch-jdbc才知道将上次抓取时间存在哪里，才可以做增量索引。

schedule的作用与crontab类似，用来固定时间执行增量导数据，具体用法参看文档活着crontab。

## 查看结果
http://localhost:9200/article/blog/_search?q=test

在配置elasticsearch-jdbc的过程中，查看日志很重要。日志文件在bin目录下的logs里，可以修改log4j2.xml文件，把日志等级改为debug以查看更多日志。

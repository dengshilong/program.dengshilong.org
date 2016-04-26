title: Spark初体验
date: 2016-04-26 22:15:55
tags:
    - Spark
categories:
    - 大数据
---
因为Oryx推荐引擎需要用到Spark, 所以开始了解Spark, 

按照[使用Spark MLlib给豆瓣用户推荐电影](http://colobu.com/2015/11/30/movie-recommendation-for-douban-users-by-spark-mllib/)写了一个[Python版本](https://github.com/dengshilong/douban_recommender), 算是有了一个初步了解。只是不知道推荐效果怎样，关键是不好测试效果。

使用的过程中遇到一个问题

### org.apache.hadoop.mapred.InvalidInputException: Input path does not exist: hdfs://localhost:9000/user/long/README.md
这是在执行[官方文档例子quickstart例子](http://spark.apache.org/docs/latest/quick-start.html)时遇到，
```
>>> textFile = sc.textFile(&quot;README.md&quot;)
>>> textFile.count()
```
一直想不通，后来想到在测试Oryx的例子时，在conf/spark-env.sh里配置了HADOOP_CONF_DIR，把它注释掉即可。

而之所以之前配置了HADOOP_CONF_DIR, 是因为在执行Oryx的例子时，会使用bin/spark-submit --master yarn-client提交，此时如果没有配置HADOOP_CONF_DIR, 会报Exception in thread "main" java.lang.Exception: When running with master 'yarn-client' either HADOOP_CONF_DIR or YARN_CONF_DIR must be set in the environment.错误。

参考文章
* http://spark.apache.org/docs/latest/
* https://www.codementor.io/spark/tutorial/building-a-recommender-with-apache-spark-python-example-app-part1
* http://colobu.com/2015/11/30/movie-recommendation-for-douban-users-by-spark-mllib/

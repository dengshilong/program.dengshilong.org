title: Hadoop Yarn安装
date: 2016-04-20 17:13:06
tags: 
    - Hadoop
    - Yarn
categories:
    - 软件安装
    
---
这里使用Hadoop 2.7.2, 在Mac上安装， 如果按照[官方文档](http://hadoop.apache.org/docs/current/hadoop-project-dist/hadoop-common/SingleCluster.html#Pseudo-Distributed_Operation)一步步来，是可以安装成功的。但如果漏了一些步骤，就会出现问题。



## Input path does not exist
最后查找日志，发现原因是
`/bin/bash: /bin/java: No such file or directory`

解决办法是将JAVA_HOME加入到etc/hadoop/hadoop-env.sh即可

## org.apache.hadoop.hdfs.server.datanode.DataNode: java.io.IOException: Incompatible 
原因是多次运行`bin/hdfs namenode -format`, 导致namenode的version和datanode的version不一致。

解决办法是修改datanode的version.
具体参考[http://blog.csdn.net/wanghai__/article/details/5752199](http://blog.csdn.net/wanghai__/article/details/5752199)

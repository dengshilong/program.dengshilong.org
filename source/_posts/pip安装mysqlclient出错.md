title: pip安装mysqlclient出错
date: 2016-12-25 21:06:57
tags:
    - pip
    - mysqlclient
categories:
---
pip安装mysqlclient时报如下错误，
```
/bin/sh: mysql_config: command not found，
```
在[stackoverflow](http://stackoverflow.com/questions/5178292/pip-install-mysql-python-fails-with-environmenterror-mysql-config-not-found)上找到如下解决办法
```
yum install python-devel mysql-devel
```

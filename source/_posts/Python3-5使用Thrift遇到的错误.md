title: Python3.5使用Thrift遇到的错误
date: 2016-12-13 22:25:21
tags:
    - Thrift
    - Python
categories:
---
在使用Thrift时，遇到TypeError: string argument expected, got 'bytes'错误。在[stackoverflow](http://stackoverflow.com/questions/32229690/apache-thrift-python-3-support)上，找到使用饿了吗的[thriftpy](https://github.com/eleme/thriftpy)库解决问题。

之后遇到TSocket read 0 bytes错误，原因是传了null值给字符串类型，改成空字符串, 解决问题。

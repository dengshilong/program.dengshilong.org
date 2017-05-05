title: thrift错误之no-handler-for-logger
date: 2017-05-05 21:07:16
tags:
    - Python
    - Thrift
categories:
---
在使用Python的thrfit库时，提示No handlers could be found for logger "thrift.server.TServer"，莫名奇妙，加了logging配置后，`logging.basicConfig(level=logging.INFO)`, 问题就解决了。

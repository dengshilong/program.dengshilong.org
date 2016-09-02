title: Scrapy日志设置
date: 2016-09-02 16:56:27
tags:
    - Scrapy
    - Python
categories:
    - Python
---
兼任运维后，爬虫这边的任务也要我处理了。发现之前的开发连日志都没有配置，纠错特别麻烦。查看[Scrapy logging](http://doc.scrapy.org/en/latest/topics/logging.html#topics-logging-settings), 找到解决的办法，原来还是很简单的。

查看logging配置，发现只要配置LOG_FILE和LOG_FORMAT即可。

在settings中添加配置如下
```
LOG_FILE='logs/spider.log'
LOG_FORMAT= '%(levelname)s %(asctime)s [%(name)s:%(module)s:%(funcName)s:%(lineno)s] [%(exc_info)s] %(message)s'
```

其中LOG_FILE指定日志路径，而LOG_FORMAT指定日志格式。因为默认的LOG_FORMAT是没有输出日志的行数，所以这里增加了行数设置。

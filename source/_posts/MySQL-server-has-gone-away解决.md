title: MySQL server has gone away解决
date: 2016-09-26 21:03:08
tags:
    - MySQL
    - Thrift
categories:
---
之前测试服务器上的Thrift服务每天都报
OperationalError: (2006, 'MySQL server has gone away')错误，但正式服务器就不会，在网上找了很久还是没找到解决的办法。

最后在[(2006, 'MySQL server has gone away') in django1.6 when wait_timeout passed](https://code.djangoproject.com/ticket/21597)找到如下回答:


> If you hit this problem and don't want to understand what's going on, don't reopen this ticket, just do this:
> * RECOMMENDED SOLUTION: close the connection with from django.db import connection; connection.close() when you know that your program is going to be idle for a long time.
> * CRAPPY SOLUTION: increase wait_timeout so it's longer than the maximum idle time of your program.

> In this context, idle time is the time between two successive database queries.

这里说对于这个问题，有两种做法，一种是关闭连接， 另一种是设置wait_timeout大于空闲时间。从这里明白原因，因为测试服务器没人访问，所以会断开连接，而正式服务器一直有人访问，所以不会。

关闭连接的话不想采用，不能每次使用都关闭连接。第二种也不采用。于是只好设置一个crontab任务，定时去访问Thrift服务。

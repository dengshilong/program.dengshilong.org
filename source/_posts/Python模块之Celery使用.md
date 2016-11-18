title: Python模块之Celery使用
date: 2016-11-18 20:57:49
tags:
    - Python
    - Celery
categories:
---
WORD文档转成PDF需要一定时间，于是异步任务派上了用场，第一选择当然是[Celery](http://docs.celeryproject.org/en/latest/index.html). Celery是用Python编写的分布式任务队列，简单，好用。

按照[Using Celery with Django](http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html#using-celery-with-django)里的介绍，很容易就配置好Celery。另外，当需要定时执行一些任务时，需要添加[django-celery-beat](http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html#django-celery-beat-database-backed-periodic-tasks-with-admin-interface)这个库，同样很好用。

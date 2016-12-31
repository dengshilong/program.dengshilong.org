title: Celery之not-json-serializable错误
date: 2016-12-31 19:40:39
tags:
    - Python
    - Celery
categories:
---
在使用Celery时遇到了object is not JSON serializable错误，参考[setting-task_serializer](http://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-task_serializer), 决定使用pickle来序列化, 添加
```
CELERY_TASK_SERIALIZER = 'pickle'
```
解决问题。

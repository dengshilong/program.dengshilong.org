title: Celery4定时任务问题
date: 2018-03-21 19:58:11
tags:
    - Celery
categories:
---
在[Celery定时任务](http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html)里介绍，配置定时任务使用crontab, 并设置timezone。于是配置了timezone="Asia/Shanghai", 然而时间总是偏差8个小时，在[Cannot use local time for cron schedules and UTC for solar schedules](https://github.com/celery/django-celery-beat/issues/57#issuecomment-372083445)里找到解决的办法。原来问题的根源是Celery里的now函数定义出错了。查看now函数的实现
```
def now(self):
    """Return the current time and date as a datetime."""
    from datetime import datetime
    return datetime.utcnow().replace(tzinfo=self.timezone)
```
改成
```
 def now(self):
    """Return the current time and date as a datetime."""
    from datetime import datetime
    return datetime.now(self.timezone) 
```
就没问题了。
查看[datetime.now](https://docs.python.org/2/library/datetime.html#datetime.datetime.now)的实现, 当tz不为空时, datetime.now(tz) 等于tz.fromutc(datetime.utcnow().replace(tzinfo=tz))。

title: Django之migrations
date: 2016-07-16 23:08:29
tags:
    - Django
    - migrations
categories:
    - 编程
---
Django提供的[migrations](https://docs.djangoproject.com/ja/1.9/topics/migrations/)功能将项目中的model与数据库表同步，方便开发。

* makemigrations app_name 生成某个app的migrations
* migrate [app_label] [migration_name]使某个app的migrations生效，当加上--fake时，假装执行migrations，实际并不执行
* sqlmigrate app_label migration_name 列出某个migrations的sql语句

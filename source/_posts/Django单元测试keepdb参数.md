title: Django单元测试keepdb参数
date: 2018-06-19 19:23:39
tags:
    - Django
categories:
---
在编写单元测试时，每次重新创建MySQL数据库表都花费很长时间，于是在表结果不变的情况下，想使用keepdb参数，即执行
`python manage.py test --keepdb`, 会报如下错误

```
Using existing test database for alias 'default'...
Got an error creating the test database: (1064, "You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'CREATE DATABASE IF NOT EXISTS `test_tdcmdb` CHARACTER SET utf8mb4;\n             ' at line 2")
```

查找错误来源，在django.db.backends.mysql.creation.py里的_execute_create_test_db函数中，
将

```
cursor.execute('''
    SET @_tmp_sql_notes := @@sql_notes, sql_notes = 0;
    CREATE DATABASE IF NOT EXISTS %(dbname)s %(suffix)s;
    SET sql_notes = @_tmp_sql_notes;
    ''' % parameters)
```

改成

```
cursor.execute('''
        CREATE DATABASE IF NOT EXISTS %(dbname)s %(suffix)s;
                ''' % parameters)
```

后，问题得到解决。

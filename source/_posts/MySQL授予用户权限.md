title: MySQL授予用户权限
date: 2016-12-25 21:43:32
tags:
    - MySQL
categories:
---
给应用创建数据库后，新建用户，之后就是给用户授予相应的权限, 参考[grant-database-privileges](http://dev.mysql.com/doc/refman/5.7/en/grant.html#grant-database-privileges)文档，授予整个数据库权限为`GRANT ALL ON mydb.* TO 'someuser'@'somehost';`, 具体可以看文档

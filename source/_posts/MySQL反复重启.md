title: MySQL反复重启
date: 2016-08-27 12:07:21
tags:
    - MySQL
categories:
---
最近测试服务器的数据库反复重启，产看日志, 提示
```
InnoDB: Log scan progressed past the checkpoint lsn 377750615222
InnoDB: The log sequence number in ibdata files does not match
InnoDB: the log sequence number in the ib_logfiles!
InnoDB: Database was not shut down normally!
```
之后无知的把ib_logfile1和ib_logfile2删掉，数据库依然反复重启。查看[MySQL文件目录格式及存放位置](http://blog.itpub.net/7220098/viewspace-1136064/)才知道这两个文件还是有用的。

之后想到一个办法是重建数据库，也就是将SQL全部导出，之后再重新导入。在使用mysqldump导出数据时，老是提示`mysqldump: Error 2013: Lost connection to MySQL server during query when dumping table`, 原因还是数据库重启了。

参考官网[forcing-innodb-recovery]
(https://dev.mysql.com/doc/refman/5.5/en/forcing-innodb-recovery.html), 在/etc/my.cnf里配置innodb_force_recovery=3, 将数据库的SQL成功导出。

修改/etc/my.cnf里的datadir，在新的目录里重启MySQL, 之后使用mysql导入数据，数据库终于正常。

使用mysqldump导出test这个数据库的命令
```
mysqldump -h 127.0.0.1 -u root -p123456 test > test.sql
```
而使用mysql命令行工具导入
```
mysql -h 127.0.0.1 -u root -p123456 test < test.sql
```

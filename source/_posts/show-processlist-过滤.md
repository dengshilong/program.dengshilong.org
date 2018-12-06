title: show processlist 过滤
date: 2018-12-06 19:10:14
tags:
    - MySQL
categories:
---
想对show processlist命令的结果进行过滤，分组操作，不支持。在[The INFORMATION_SCHEMA PROCESSLIST Table](https://dev.mysql.com/doc/refman/5.7/en/processlist-table.html)里可以看到SHOW FULL PROCESSLIST 和 SELECT * FROM INFORMATION_SCHEMA.PROCESSLIST效果是相等的，于是可以在PROCESSLIST表上进行过滤分组操作。

* 需要对host进行统计 select substring_index(host,':' ,1) as server, count(*) from information_schema.processlist  group by server;


* 查询执行时间超过2分钟的线程，然后拼接成 kill 语句 select concat('kill ', id, ';') from information_schema.processlist where command != 'Sleep' and time > 2*60 order by time desc 

## 参考资料

* [学会用 Mysql show processlist 排查问题](https://xu3352.github.io/mysql/2017/07/08/msyql-show-full-processlist)
* [The INFORMATION_SCHEMA PROCESSLIST Table](https://dev.mysql.com/doc/refman/5.7/en/processlist-table.html)

title: MySQL显示链接数
date: 2016-09-02 16:59:40
tags:
    - MySQL
categories:
    - 数据库
---
最近服务时不时的会卡顿，不知道什么原因。下班之后突然想到速度慢，一般都出在数据库上。于是想到查看MySQL链接数，网上查到执行`show processlist；`即可。

在卡顿时，查询结果中发现以下可疑连接，如下
```
 Waiting for table level lock | UPDATE `sku` SET  `view_num` = `sku`.`view_num` + 1 WHER |         0 |             0 |         1 |
 
Waiting for table level lock | SELECT `sku`.`id`, `sku`.`name`, `sku`.`dosage_form`, `sku`.`specs`, `sku`.`factory`, `sku`.`categor |         0 |             0 |         1 |
```

在淘宝的MySQL资料[MySQL 锁问题最佳实践](http://mysql.taobao.org/monthly/2016/03/10/)里找到'table level lock'的原因，是因为MyISAM，引发table level lock wait。查看建表语句，果然是MyISAM引擎, 将它转成InnoDB即可解决问题。

上面使用`show processlist`命令显示不完全，可以加上full, 即执行`show full processlist`

参考[Converting Tables from MyISAM to InnoDB](http://dev.mysql.com/doc/refman/5.5/en/converting-tables-to-innodb.html), 执行`ALTER TABLE table_name ENGINE=InnoDB;`即可转换。

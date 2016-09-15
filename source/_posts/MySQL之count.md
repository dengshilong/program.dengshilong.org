title: MySQL之count
date: 2016-09-15 17:02:26
tags:
    - MySQL
    - count
categories:
    - 数据库
---
MySQL提供了count命令来统计表中的记录数, 使用起来非常方便。但加上where条件的count命令有时会很慢，此时需要优化。

最近在项目中就遇到这个问题。看下面两个SQL的查询结果。
```
mysql> SELECT COUNT(*) FROM user WHERE user.is_active = 1;
+-----------+
| COUNT(id) |
+-----------+
|    239563 |
+-----------+
1 row in set (0.21 sec)

mysql> select count(*) from sku_pro where is_agent=1;
+-----------+
| count(id) |
+-----------+
|   1253535 |
+-----------+
1 row in set (0.11 sec)
```

看到这个结果，肯定会很吃惊。user表的数据比sku_pro表的数据少很多，但执行时间却比它长，匪夷所思。查看两个表结构，两个表都是MyISAM引擎，看到的差别是user表61个字段，而sku_pro表16个字段。

在网上找各种资料，没有找到问题的答案。于是请教同学，同学提示说看数据大小，如果数据大的，读到内存需要花费更多的IO，这样会更慢一些。但发现两个表数据大小差不多。

在查看show table status的结果时，发现user表的RowFormat是Dynamic, 而sku_pro表的是Fixed, 于是查看user表结构，发现很多字段是varchar字段，于是猜测在Dynamic时，要查找到字段的值，需要计算便宜量，这样速度更慢。在[MySQL Optimization: Faster Selects with MyISAM fixed row format](http://www.soliantconsulting.com/blog/2012/09/mysql-optimization-faster-selects-myisam-fixed-row-format)一文中有提到这个问题。

但是如果不想改变RowFormat又该怎么做？在StackoverFlow上提了这个[问题](http://stackoverflow.com/questions/39481876/why-count-query-runs-slower-in-less-data-than-more-data-in-myisam/39482638), 很快得到解答，只需要创建索引即可，需要注意索引里有加上id字段，
```
CREATE INDEX is_active ON user (is_active,id);
```
这个不是创建
```
CREATE INDEX is_active ON user (is_active);
```
在解答中有提到，这个索引会被忽略。

参考资料:
* [COUNT(*) vs COUNT(col)](https://www.percona.com/blog/2007/04/10/count-vs-countcol/)
* [在MySQL的InnoDB存储引擎中count(*)函数的优化](https://segmentfault.com/a/1190000003793230)

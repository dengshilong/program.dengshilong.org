title: 'MySQL的timestamp类型 '
tags:
  - MySQL
  - timestamp
  - 自动更新
id: 677
categories:
  - 数据库
date: 2014-04-12 15:03:30
---

在数据库应用中，时间字段是极为常用的，而timestamp因为有一个很好的特性，所以经常用到。例如将timestamp设置为NOT NULL DEFAULT CURRENT_TIMESTAMP时，在数据第一次插入时，时间会自动设置为当前时间。

而如果再加上ON UPDATE CURRENT_TIMESTAMP，也就是将timestamp类型设置为 NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP，这样在更新数据时，就会自动更新为当前时间。如此，就没有必要在更新数据时，使用now函数。

最近在做一个项目，令我意外的是，一个同事竟然不知道有这个类型，所以在更新数据时，他要使用now函数。他说在数据结构设计时，不会关心具体数据库提供的特性。即便如此，我还是认为，数据结构设计还是要接地气的。
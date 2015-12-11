title: 如何实现site查询
tags:
  - site查询
id: 949
categories:
  - 搜索引擎
date: 2014-10-27 21:55:46
---

在Solr的索引记录里看到，很多HostName是逆序的，如news.qq.com记录成moc.qq.swen, www.qq.com记录成moc.qq.www,moc.qq,finance.qq.com记录成moc.qq.ecnanif。后来才知道，这是为了实现像google那样的site功能.

site功能就是要查找索引中某一域名下的记录。一个实现办法就是实现上面的逆序存储。如此，要找出qq.com下的所有记录只需要用moc.qq.*去比较HostName即可。
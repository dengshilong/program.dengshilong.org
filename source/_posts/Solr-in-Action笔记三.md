title: Solr in Action笔记三
tags:
  - solr
id: 979
categories:
  - 搜索引擎
date: 2014-12-14 22:12:05
---

Solr关键概念

1.反向索引
2.检索词和布尔查询：
并查询：
+new +house 或者
new AND house
或查询：
new house 或者
new OR house
排除查询:
new house –rental 或者
new house NOT rental
短语查询：
“new home” OR “new house”
3 bedrooms” AND “walk in closet” AND “granite countertops”
分组查询：
New AND (house OR (home NOT improvement NOT depot NOT grown))
(+(buying purchasing -renting) +(home house residence –(+property -bedroom)))

对于短语查询，之所以可以实现，是因为在反向索引中保存了词在文档中的位置信息。

3.模糊查询
通配符查询：
如果需要查询以offic开头的词，只需要查询 offic*
如果要使用通配符在开头的查询，如 *ing,则需要将ReversedWildcardFilterFactory添加到字段分析链中

范围查询：
yearsOld:[18 TO 21] 18 <= x <= 21
yearsOld:{18 TO 21} 18 < x < 21
yearsOld:[18 TO 21} 18 <= x < 21
created:[2012-02-01T00:00.0Z TO 2012-08-02T00:00.0Z]

编辑距离查询：
administrator~ 默认编辑距离为1
administrator~1 编辑距离为1
administrator~2  编辑距离为2

临近查询：
“chief officer”~1 距离为1
例如: “chief executive officer”, “officer chief”

4.相关性：
Solr默认相关性，距离看文档

5.准确率和召回率
准确率说的是一次查询中，查询结果有多少是相关的比率
召回率说的是一次查询中，有多少相关结果被返回的比率

一般来说，搜索引擎都是尽量在二者中寻求一个平衡

6.Solr的一些局限
Solr无法执行想数据库查询那样复杂的查询
当更新一个跨越很多个文档的字段时，Solr将很麻烦
对于返回许多文档的查询，Solr的性能将会下降
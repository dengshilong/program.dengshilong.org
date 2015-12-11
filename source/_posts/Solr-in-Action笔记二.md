title: Solr in Action笔记二
tags:
  - solr
id: 957
categories:
  - 搜索引擎
date: 2014-11-16 19:56:07
---

初识Solr

1.安装Solr,
方法一，下载源码，编译，安装，这个单独介绍
方法二，下载二进制文件，解压，即可。

2.启动Solr
进入example目录,允许 java -jar start.jar，默认监听8983端口，访问http://localhost:8983/solr看看是否启动。
若端口被占用，修改启动端口即可，java -Djetty.port=8080 -jar start.jar 。

3.查询
Solr后台，查询表单的参数意义示例
字段 值 意义
q iPod 查询词
fq manu:Belkin 过滤，只显示manu中有Belkin的结果
sort price asc 排序，价格从低到高排列
start 0 分页参数,相当于mysql中的offset,即从第几条结果开始显示
rows 10 分页参数,想到与mysql中的limit,即总共显示几条结果
fl name,price,features,score 需要显示的字段
df text 默认搜索字段，对于没有制定搜索字段的查询，默认查询text字段
wt xml 返回结果显示格式，还有json,csv等多种格式供选择

4.相关性排序
可以对查询词进行加权，改变排序结果，如查询词“iPod power"变成"iPod power^2"，则power的权重是iPod的两倍

5.分页
使用start和rows参数，每页显示条数尽量小，因为需要都去返回字段的值，条数越多，速度越慢

6.排序
对返回结果使用如 price asc等进行排序

7.提供的搜索组件
dismax 如何翻译，待查
edismax 如何翻译，待查
hl 高亮
facet 平面搜索
spatial 地理位置搜索
spellchecking 拼写检查
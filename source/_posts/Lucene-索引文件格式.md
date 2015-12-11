title: Lucene 索引文件格式
tags:
  - Lucene
  - 索引
id: 959
categories:
  - 搜索引擎
date: 2014-11-19 21:56:33
---

随着对Solr的进一步深入，自然就想了解Lucene的索引文件格式。之前写的段合并小工具不知怎么不起作用了(后来发现是没有更新代码)，于是把觉先的《Lucene源码剖析》又翻出来看，顺便看了一下 Lucene索引格式。Solr使用的是1.4的，查看文件格式，与Lucene2.9的文件格式相差不大，依然有参考价值。

到索引目录下查看，一共有如下几种文件格式。对照[http://lucene.apache.org/core/2_9_4/fileformats.html](http://lucene.apache.org/core/2_9_4/fileformats.html)，知道每一种格式的大概用途。
segments.gen, segments_N Segments File 主要保存索引段信息
.fnm Fields 域的元数据信息文件，保存域信息
.fdx Field Index 域数据索引文件，保存指向域数据文件的指针，方便快速访问域数据文件
.fdt Field Data 域数据文件，保存每个文档的字段,域的真正值就是在这里保存
.tis Term Infos 词典文件,记录索引词的信息
.tii Term Info Index 词典索引文件，记录到tis文件的指向，主要是为了加快访问词典文件
.frq Frequencies 文档号与词频文件，记录索引词在文档中的词频
.prx Positions 词位置信息文件，记录索引词的位置信息
.nrm Norms 标准化因子文件，记录文档和域的权重
.tvx Term Vector Index 词向量索引文件，保存到词向量文档文件和词向量域文件的指针
.tvd Term Vector Documents 词向量文档文件，记录文档第一个域与其它域的偏移
.tvf Term Vector Fields 词向量域文件，记录域级别的词向量
.del Deleted Document 记录哪个文档被删除

还有.cfs文件，也即是Compound File，当将所有索引文件合成一个文件时才会出现，主要是减少文件句柄。
write.lock,用来互斥的写索引文件。
而.tvx,tvd,tvf只有在启用词向量时才会出现。
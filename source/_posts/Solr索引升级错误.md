title: Solr索引升级错误
tags:
  - solr
  - 升级
  - 索引
id: 952
categories:
  - 搜索引擎
date: 2014-11-08 15:53:58
---

最近需要将Solr从1.4升级到4.8，于是需要将索引数据进行升级，而1.4无法直接升级到4.8，需要经过如下转化。从1.4升级到3.6，3.6升级到4.0，4.0升级到4.8。有几个引擎的数据升级很顺利，可是也有那么几个引擎的数据升级过程中出现了错误。

错误都出现在4.0升级到4.8时。调用栈如下：
Caused by: java.lang.IllegalArgumentException: maxValue must be non-negative (got: -1)
        at org.apache.lucene.util.packed.PackedInts.bitsRequired(PackedInts.java:1180)
        at org.apache.lucene.codecs.lucene41.ForUtil.bitsRequired(ForUtil.java:243)
        at org.apache.lucene.codecs.lucene41.ForUtil.writeBlock(ForUtil.java:164)
        at org.apache.lucene.codecs.lucene41.Lucene41PostingsWriter.addPosition(Lucene41PostingsWriter.java:368)
        at org.apache.lucene.codecs.PostingsConsumer.merge(PostingsConsumer.java:123)
        at org.apache.lucene.codecs.TermsConsumer.merge(TermsConsumer.java:164)
        at org.apache.lucene.codecs.FieldsConsumer.merge(FieldsConsumer.java:72)
        at org.apache.lucene.index.SegmentMerger.mergeTerms(SegmentMerger.java:389)
        at org.apache.lucene.index.SegmentMerger.merge(SegmentMerger.java:112)
        at org.apache.lucene.index.IndexWriter.mergeMiddle(IndexWriter.java:4132)
        at org.apache.lucene.index.IndexWriter.merge(IndexWriter.java:3728)
        at org.apache.lucene.index.ConcurrentMergeScheduler.doMerge(ConcurrentMergeScheduler.java:405)
        at org.apache.lucene.index.ConcurrentMergeScheduler$MergeThread.run(ConcurrentMergeScheduler.java:482)

看代码后，在PostingsConsumer 120行附近，final int position = postingsEnum.nextPosition();，这个position是负的，所以报错。看这附近的代码，知道是对索引词的在文档中的位置信息进行压缩。可是词在文档中的位置不应该是负的，于是报错。问题是，为什么这里会出现负的位置，只能解释是数据问题。一个解决的办法是跳过为负的位置，如此升级确实成功了，只是不知道有没有什么副作用。
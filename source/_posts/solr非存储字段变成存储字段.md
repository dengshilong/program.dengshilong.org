title: solr非存储字段变成存储字段
tags:
  - fieldcache
  - solr
  - 段合并
id: 917
categories:
  - 搜索引擎
date: 2014-09-25 23:01:28
---

试想这样一种情形，一个publish_time，原先是只索引不保存，运行了很长一段时间后，发现需要返回这个字段，于是改成既索引又保存。这样新进来的数据就可以返回这个字段的值，可是原先保存的数据将无法返回这个字段的值，因为没有保存。那如何解决这个问题？

一个解决的办法是将数据重新跑一遍，重建索引，这样所有的数据都可以返回publish_time这个字段。想想还有没有其它办法，看到建了索引，这样还是有办法可以拿到数据，一个解决的办法是读fiedcache. 索引加载时，会在fieldcache里记录字段信息，这样可以提高字段查询的速度。事实上，在上述例子中，进行publish_time字段查询时，就可以拿到所有数据的publish_time字段信息,而这些信息就是来自于fieldcache.

于是找到了一个切入点，在进行段合并时，将之前没有保存的字段信息从fieldcache中读出，写到新的段中，这样新生成的段中,所有数据都会有publish_time字段信息。

于是问题的关键就变成了如何处理在段合并时，读取fieldcache信息，并且增加到新段中.从《Lucene原理与代码分析》中可以知道，段合并主要是在SegmentMerger中完成,具体是在copyFieldsWithDeletions和copyFieldsNoDeletions中。看名字就可以知道这两个函数是对应的，所以只要讨论其中一个就行了。在合并时主要分两种情况，一种是合并的段所有字段的顺序和个数都是一样的，这样只要将段数据复制到新段中即可，另一种则需要像添加一篇新文档一样将段中的文档一篇篇添加，具体体现就在fieldsWriter.addDocument(doc);这句。

对于后一情况，需要从fieldcache中读取之前没有保存的字段，如FieldCache.DEFAULT.getInts(reader, fieldName)，这里的reader是一个SegmentReader实例, fieldName则是字段名,这样就可以得到字段的值,。而文档已经由Document doc = reader.document(docCount,  fieldSelectorMerge)读出，之后构建一个Field将它添加到文档中，并将文档添加到段中即可.

需要注意的是,reader一定要加载索引，否则会报，terms index was not loaded when this reader was created错误.

还有就是,对于int,double等数值型数据,需要调用Field(String name, byte[] value)方法，也就是先将int,double等转化成byte[]数组，之后再构建。具体转化方法参见[int,double等转化成byte数组](http://program.dengshilong.org/2014/09/24/intdouble%E7%AD%89%E8%BD%AC%E5%8C%96%E6%88%90byte%E6%95%B0%E7%BB%84/).
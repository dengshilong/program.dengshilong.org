title: solr非存储字段变成存储字段解决代码
tags:
  - fieldcache
  - solr
id: 961
categories:
  - 搜索引擎
date: 2014-11-19 22:22:13
---

看来这一段小代码还是有点用的，还是开源出来吧，免得再造轮子。注意，修改时基于Solr1.4,其它版本进行相应修改即可。

主要修改了两个类IndexWriter, SegmentMerger.添加辅助类ByteUtil,TypeUtil，Constant。

修改类IndexWriter:
在方法private int mergeMiddle(MergePolicy.OneMerge merge)里，
 将SegmentReader初始化 SegmentReader reader = merge.readers[i] =  readerPool.get(info, merge.mergeDocStores,MERGE_READ_BUFFER_SIZE, -1);
 修改成
``` 
String temp = System
       .getProperty(Constant.DOCUMENT_MERGE_OPTION);
boolean documentMerge =  temp != null && temp.equals("true") ? true
       : false;
if (documentMerge) {
   merge.readers[i] = readerPool.get(info, merge.mergeDocStores,
           MERGE_READ_BUFFER_SIZE,
           IndexReader.DEFAULT_TERMS_INDEX_DIVISOR);
} else {
   merge.readers[i] = readerPool.get(info, merge.mergeDocStores,
           MERGE_READ_BUFFER_SIZE,
           -1);
}
SegmentReader reader = merge.readers[i];
```
 这是因为如果需要读FieldCache,则需要加载内存，否则会报错。而readerPool.get这个函数内有这样一个判断
``` 
if (termsIndexDivisor != -1 && !sr.termsIndexLoaded()) {
 // If this reader was originally opened because we
 // needed to merge it, we didn't load the terms
 // index.  But now, if the caller wants the terms
 // index (eg because it's doing deletes, or an NRT
 // reader is being opened) we ask the reader to
 // load its terms index.
 sr.loadTermsIndex(termsIndexDivisor);
}
```
    设置第四个参数为IndexReader.DEFAULT_TERMS_INDEX_DIVISOR，SegmentReader就会增加索引
修改类SegmentMerger:
在mergeFields函数里,将copyFieldsWithDeletions和copyFieldsNoDeletions增加一个参数 boolean documentMerge
 参数的值由如下语句得到
``` java
 String temp = System.getProperty(Constant.DOCUMENT_MERGE_OPTION);
 boolean documentMerge =  temp != null && temp.equals("true") ? true : false;
```

 函数copyFieldsWithDeletions和copyFieldsNoDeletions是对应的，这里只拿copyFieldsNoDeletions举例。
 在copyFieldsNoDeletions里，读取FieldCache的主要工作在以下这个判断语句里完成.
``` 
if (documentMerge) {
   //Update Dengshilong 2014-09-25
   //here is where  documentMerge and read FieldCache actually do
   //read fields and types from start parameters
   //for every field ,read value from FieldCache , 
   //for numerical field use the correspond byte transform method to build a Field
   String fieldNamesStr = System
           .getProperty(Constant.DOCUMENT_MERGE_FIELDS);
   String typesStr = System
           .getProperty(Constant.DOCUMENT_MERGE_TYPES);
   String[] fieldNames = fieldNamesStr.split(",");
   String[] types = typesStr.split(",");
   for (; docCount < maxDoc; docCount++) {
       // NOTE: it's very important to first assign to doc then
       // pass it to
       // termVectorsWriter.addAllDocVectors; see LUCENE-1282
       Document doc = reader.document(docCount,
               fieldSelectorMerge);
       Map typeMap = TypeUtil.TYPE_MAP;
       for (int i = 0; i < fieldNames.length; i++) {
           String fieldName = fieldNames[i];
           String type = types[i];
           Fieldable field = (Fieldable) doc
                   .getFieldable(fieldName);
           if (field == null) {
               Types t = (Types) TypeUtil.TYPE_MAP.get(type);
               switch(t) {
               case INTEGER:
                   int[] vi = FieldCache.DEFAULT.getInts(reader, fieldName);
                   Field fi = new Field(fieldName, ByteUtil.toArr(vi[docCount]), Store.YES);
                   doc.add(fi);
                   break;
               case LONG:
                   long[] vl = FieldCache.DEFAULT.getLongs(reader, fieldName);
                   Field fl = new Field(fieldName, ByteUtil.toArr(vl[docCount]), Store.YES);
                   doc.add(fl);
                   break;
               case FLOAT:
                   float[] vf = FieldCache.DEFAULT.getFloats(reader, fieldName);
                   Field ff = new Field(fieldName, ByteUtil.toArr(vf[docCount]), Store.YES);
                   doc.add(ff);
                   break;
               case DOUBLE:
                   double[] vd = FieldCache.DEFAULT.getDoubles(reader, fieldName);
                   Field fd = new Field(fieldName, ByteUtil.toArr(vd[docCount]), Store.YES);
                   doc.add(fd);
                   break; 
               }
           } else {
               continue;
           }    
       }

       fieldsWriter.addDocument(doc);
       checkAbort.work(300); 
   }
}
```
增加类ByteUtil用于int,double等数值型转化为byte[]数组;
``` 
package org.apache.lucene.util;
//The transform method is copy from TrieField.java
public class ByteUtil {
    public static int toInt(byte[] arr) {
        return (arr[0] << 24) | ((arr[1] & 0xff) << 16)
                | ((arr[2] & 0xff) << 8) | (arr[3] & 0xff);
    }

    public static long toLong(byte[] arr) {
        int high = (arr[0] << 24) | ((arr[1] & 0xff) << 16)
                | ((arr[2] & 0xff) << 8) | (arr[3] & 0xff);
        int low = (arr[4] << 24) | ((arr[5] & 0xff) << 16)
                | ((arr[6] & 0xff) << 8) | (arr[7] & 0xff);
        return (((long) high) << 32) | (low & 0x0ffffffffL);
    }
    public static float toFloat(byte[] arr) {
        return Float.intBitsToFloat(toInt(arr));
    }
    public static double toDouble(byte[] arr) {
        return Double.longBitsToDouble(toLong(arr));
    }

    public static byte[] toArr(int val) {
        byte[] arr = new byte[4];
        arr[0] = (byte) (val >>> 24);
        arr[1] = (byte) (val >>> 16);
        arr[2] = (byte) (val >>> 8);
        arr[3] = (byte) (val);
        return arr;
    }

    public static byte[] toArr(long val) {
        byte[] arr = new byte[8];
        arr[0] = (byte) (val >>> 56);
        arr[1] = (byte) (val >>> 48);
        arr[2] = (byte) (val >>> 40);
        arr[3] = (byte) (val >>> 32);
        arr[4] = (byte) (val >>> 24);
        arr[5] = (byte) (val >>> 16);
        arr[6] = (byte) (val >>> 8);
        arr[7] = (byte) (val);
        return arr;
    }

    public static byte[] toArr(float val) {
        return toArr(Float.floatToRawIntBits(val));
    }

    public static byte[] toArr(double val) {
        return toArr(Double.doubleToRawLongBits(val));
    }
}
```
增加类TypesUtil，定义了INTEGER等类型常量
``` 
package org.apache.lucene.util;
import java.util.HashMap;
import java.util.Map;
//the types is copy form TrieField.java
public class TypeUtil {
    public enum Types {
        INTEGER,
        LONG,
        FLOAT,
        DOUBLE,
   }
   public final static Map TYPE_MAP = new HashMap() { {    
        put("int", Types.INTEGER);    
        put("tint", Types.INTEGER);
        put("long", Types.LONG); 
        put("tlong", Types.LONG);
        put("float", Types.FLOAT);
        put("tfloat", Types.FLOAT);
        put("double", Types.DOUBLE);
        put("tdouble", Types.DOUBLE);
   }}; 
}
```
增加类Constant,定义了三个常量
``` 
package org.apache.lucene.util;
public class Constant {
  //add for documentMerge
  public final static String DOCUMENT_MERGE_OPTION = "search.index.documentMerge";
  public final static String DOCUMENT_MERGE_FIELDS = "search.index.documentMerge.fields";
  public final static String DOCUMENT_MERGE_TYPES = "search.index.documentMerge.types";
}
```
使用：
在solr启动脚本中,添加如下参数
search.index.documentMerge 为true时表示开启强制文档合并,其它值时表示不开启
search.index.documentMerge.fields 需要读取的字段，字段之间用逗号隔开
search.index.documentMerge.types 读取字段的类型,类型间用逗号隔开,这里的类型要与上面的字段一一对应起来
举个例子：

要对PublishTime,ContentLength进行读取,而它们的字段类型分别为tint,int于是添加如下参数
-Dsearch.index.documentMerge=true -Dsearch.index.documentMerge.fields=PublishTim,ContentLength
 -Dsearch.index.documentMerge.types=tint,int

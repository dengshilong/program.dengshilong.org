title: Lucene中扩展codec功能
tags:
  - codec
  - Lucene
id: 991
categories:
  - Lucene
date: 2015-01-16 21:04:44
---

从Lucene4.0开始，提供了扩展codec功能，这个功能主要是留给想自己定义索引格式的开发者。
在此之前，有必要了解codec主要的作用，codec相关的类主要作用是读写索引。 而通过实现FilterCodec，可以很方便的定义自己的codec。 这个方便主要是可以将许多读写索引部分交给已有的codec实现，而只实现自己需要改进的部分。当然如果这样还不能满足需求 可以重新写一个codec。 

写个简单的例子更容易懂，
在Codec.java中，可以看到，读写索引主要实现以下几个方法 
``` java
 /** Encodes/decodes postings */
  public abstract PostingsFormat postingsFormat();

  /** Encodes/decodes docvalues */
  public abstract DocValuesFormat docValuesFormat();

  /** Encodes/decodes stored fields */
  public abstract StoredFieldsFormat storedFieldsFormat();

  /** Encodes/decodes term vectors */
  public abstract TermVectorsFormat termVectorsFormat();

  /** Encodes/decodes field infos file */
  public abstract FieldInfosFormat fieldInfosFormat();

  /** Encodes/decodes segment info file */
  public abstract SegmentInfoFormat segmentInfoFormat();

  /** Encodes/decodes document normalization values */
  public abstract NormsFormat normsFormat();

  /** Encodes/decodes live docs */
  public abstract LiveDocsFormat liveDocsFormat();
```
一个纯文本保存索引的codec是SimpleTextCodec,这个codec的主要目的是用来学习

下面定义自己的codec
``` java
public class HexinCodec extends FilterCodec {
    final private FieldInfosFormat myTermFieldInfoFormat;
    public HexinCodec() {
        super("HexinCodec", new Lucene46Codec());
        myTermFieldInfoFormat = new SimpleTextFieldInfosFormat();
    }
    public FieldInfosFormat fieldInfosFormat() {
        return myTermFieldInfoFormat;
    }
}
```
最后，还是让上面的例子跑起来，首先下载Lucene4.8.0的源码，之后在codecs/src/java下新建包org.apache.lucene.codecs.hexin,
在这个包下面新建类HexinCodec.java,复制上面的代码。
之后编写测试用的建索引程序Index.java 
``` java
package org.hexin;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.codecs.Codec;
import org.apache.lucene.codecs.hexin.HexinCodec;
import org.apache.lucene.codecs.lucene46.Lucene46Codec;
import org.apache.lucene.codecs.simpletext.SimpleTextCodec;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig.OpenMode;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;

import java.io.File;
import java.io.IOException;
public class Index {
    public static void main(String[] args) throws IOException {
        //Codec codec = new SimpleTextCodec();
        Codec codec = new HexinCodec();
        //Codec codec = new Lucene46Codec();
        String INDEX_DIR = "e:\\index";
        Analyzer analyzer = new StandardAnalyzer(Version.LUCENE_48);
        IndexWriterConfig iwc = new IndexWriterConfig(Version.LUCENE_48, analyzer);
        iwc.setCodec(codec);
        IndexWriter writer = null;
        iwc.setOpenMode(OpenMode.CREATE);
        iwc.setUseCompoundFile(false);
        try {
            writer = new IndexWriter(FSDirectory.open(new File(INDEX_DIR)), iwc);
            Document doc = new Document();
            doc.add(new TextField("title", "who are you, you are a man", Field.Store.YES));
            doc.add(new TextField("content", "A long way to go there. Please drive a car", Field.Store.NO));
            writer.addDocument(doc);
            doc = new Document();
            doc.add(new TextField("title", "are you sure", Field.Store.YES));
            doc.add(new TextField("content", "He is a good man. He is a driver", Field.Store.NO));
            writer.addDocument(doc);
            writer.commit();
            writer.close();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
    }  
}
```
编写测试用的搜索例子Search.java 
``` java
package org.hexin;
import java.io.File; 
import java.util.Date;

import org.apache.lucene.codecs.Codec;
import org.apache.lucene.codecs.simpletext.SimpleTextCodec;
import org.apache.lucene.document.Document;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.Term;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.TermQuery;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
import org.apache.lucene.store.FSDirectory;
public class Search {
    private Search() {}
    public static void main(String[] args) throws Exception {

        String index = "e:\\index";
        IndexReader reader = DirectoryReader.open(FSDirectory.open(new File(index)));
        IndexSearcher searcher = new IndexSearcher(reader);
        String queryString = "driver";
        Query query = new TermQuery(new Term("content", queryString));
        System.out.println("Searching for: " + query.toString());
        Date start = new Date();
        TopDocs results = searcher.search(query, null, 100);
        Date end = new Date();
        System.out.println("Time: "+(end.getTime()-start.getTime())+"ms");
        ScoreDoc[] hits = results.scoreDocs;
        int numTotalHits = results.totalHits;
        System.out.println(numTotalHits + " total matching documents");
        for (int i = 0; i < hits.length; i++) {
            String output = "";
            Document doc = searcher.doc(hits[i].doc);
            output += "doc="+hits[i].doc+" score="+hits[i].score;
            String title = doc.get("title");
            if (title != null) {
                output += " " + title;
            }
            System.out.println(output);
        }
        reader.close();
    }
}
```

在Eclipse中运行Index.java,此时会报错
A SPI class of type org.apache.lucene.codecs.Codec with name 'Lucene46' does not exist. You need to add the corresponding 
JAR file supporting this SPI to your classpath.The current classpath supports the following names:[]

问过定坤后，知道一个解决的办法是去官网下载已经编译过的Lucene二进制包,将其中的META-INF拷贝到core/src/java目录下，写上下面两行
org.apache.lucene.codecs.simpletext.SimpleTextCodec
org.apache.lucene.codecs.hexin.HexinCodec
此时即可运行通过。查看索引文件，有一个fld结尾的文件，其内容为文本文件,保存着字段值,这个文件就是通过SimpleTextCodec写入的，
而其它文件则是通过Lucene46Codec写入的。

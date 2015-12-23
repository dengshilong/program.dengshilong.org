title: Lucene入门例子
tags:
  - Lucene
id: 896
categories:
  - Lucene
date: 2014-08-27 21:27:13
---

开始Lucene之路,从官网下了最新的4.9.0,从先从小例子开始.
建索引
``` java
package org.dsl;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
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
        String INDEX_DIR = "e:\\index";
        Analyzer analyzer = new StandardAnalyzer(Version.LUCENE_4_9);
        IndexWriterConfig iwc = new IndexWriterConfig(Version.LUCENE_4_9, analyzer);
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
搜索
``` java
package org.dsl;
import java.io.File;
import java.util.Date;
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

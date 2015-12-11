title: Solr权限控制solrj认证
tags:
  - security
  - solr
  - solrj
id: 1000
categories:
  - 搜索引擎
date: 2015-01-22 19:44:28
---

在上篇中，我们通过在jetty中配置，是update需要进行用户名和密码认证，这篇中我们继续介绍如何在solrj中调用update

*测试添加文档 
先尝试使用solrj,编写测试程序 
``` java
String url = "http://localhost:8989/solr"; 
HttpSolrServer server = new HttpSolrServer(url); 
SolrInputDocume doc1 = new SolrInputDocument(); 
server.add(docs); 
```
提示401错误,添加用户名和密码: 
``` java
String url = "http://localhost:8989/solr"; 
HttpSolrServer server = new HttpSolrServer(url); 
HttpClientUtil.setBasicAuth((DefaultHttpClient) server.getHttpClient(), "index", "update"); 
SolrInputDocume doc1 = new SolrInputDocument(); 
server.add(docs); 
```
提示 NonRepeatableRequestException, Cannot retry request with a non-repeatable request entity. 想跟踪过去,看看错误出自哪里,没办法调到源代码,于是尝试查询. 
*测试查询文档 
将etc/webdefault.xml中对<url-pattern>/update/*</url-pattern>的限制改成,<url-pattern>/select/*</url-pattern>,编写查询代码, 
``` java
String url = "http://localhost:8989/solr"; 
HttpSolrServer server = new HttpSolrServer(url); 
SolrQuery query = new SolrQuery(); 
String q = "*:*"; 
query.setQuery(q); 
```
提示401错误,添加用户名和密码: 
``` java
String url = "http://localhost:8989/solr"; 
HttpSolrServer server = new HttpSolrServer(url); 
SolrQuery query = new SolrQuery(); 
String q = "*:*"; 
query.setQuery(q); 
```
查询成功, 

*问题解决 
不明白原因,只是猜测post的信息不能反复使用,在setBasicAuth前面有一段说明, "Currently this is not preemtive authentication. So it is 
not currently possible to do a post request while using this setting.",意思就是认证过程不是最先进行的,所以现在不能用于post,可是认证 
过程可以用于get,于是察看get的执行过程,发现它先执行一次,发现要认证,于是再执行一次,而第二次执行时会先执行认证过程. 对于post过程,如果 
可以执行同样的过程,那就可以达到目的,关键问题是"Cannot retry request with a non-repeatable request entity",于是查看solr-4470是如何 
实现的,看到HttpSolrServer里代码如下: 
    ``` java
     if (contentStream[0] instanceof RequestWriter.LazyContentStream) {
        post.setEntity(new InputStreamEntity(contentStream[0].getStream(), -1) {
          @Override
          public Header getContentType() {
            return new BasicHeader("Content-Type", contentStream[0].getContentType());
          }

          @Override
          public boolean isRepeatable() {
            return false;
          }

        });
      } else {
        post.setEntity(new InputStreamEntity(contentStream[0].getStream(), -1) {
          @Override
          public Header getContentType() {
            return new BasicHeader("Content-Type", contentStream[0].getContentType());
          }

          @Override
          public boolean isRepeatable() {
            return false;
          }
        });
      }```
修改成 
     ``` java
     HttpEntity entity = new InputStreamEntity(contentStream[0].getStream(), -1) {
         @Override
         public Header getContentType() {
             return new BasicHeader("Content-Type", contentStream[0].getContentType());
         }
         @Override
         public boolean isRepeatable() {
             return false;
         }  
     };
     entity = new BufferedHttpEntity(entity);```

在生产环境中，可以添加参数控制是否需要entity = new BufferedHttpEntity(entity);和 
HttpClientUtil.setBasicAuth((DefaultHttpClient) server.getHttpClient(), "index", "update");这两句
title: 'solr分布式搜索时设置分页的一个错误 '
tags:
  - solr
  - 分布式
  - 分页
id: 905
categories:
  - 搜索引擎
date: 2014-09-19 21:16:58
---

最近在做一个站内搜索功能,有用到一个分页功能.搜索时会传两个参数pageId和pageSize 用来指定页号与每页的条数.solr已经提供了start和rows两个参数,于是将分页参数与之对应起来,在component初始化时写了如下代码:
``` 
String pidStr = req.getParams().get(PAGE_ID);
if ( pidStr != null ) { 
    int pageId = req.getParams().getInt(PAGE_ID, 0);
    int pageSize = req.getParams().getInt(PAGE_SIZE, 10);
    pageId = (pageId > -1) ? pageId : 0; 
    pageSize = (pageSize > 0 ) ? pageSize : 10; 
    ModifiableSolrParams params = new ModifiableSolrParams(req.getParams());
    params.set(CommonParams.START, pageId * pageSize);
    params.set(CommonParams.ROWS, pageSize);
    params.set(CommonParams.WT, "json");
    params.set(CommonParams.OMIT_HEADER, "true");
    req.setParams(params);
}
```
可是一直得不到正确的结果，在后台输出日志,发现start和rows在设置了上面的值后，start和rows会用来构建新的查询,在新的查询中start会变为0,而rows会变成start与rows的和，可是之后start和rows又会变成原先的值，于是得不到想要的结果。

举个例子,假设要搜第三页,每页10条,则可设置pageId为2,pageSize为10,于是start被设置成20,rows被设置成10,之后start和rows会被用于生成向shard发送的请求,start被设置为0,rows设置为30.问题在于这个请求发出之后start的值又变成了20,rows变成了10,百思不得其解.

跟踪代码到createMainQuery函数,看到如下代码：
``` 
if (rb.shards_start > -1) {
    // if the client set shards.start set this explicitly
    sreq.params.set(CommonParams.START, rb.shards_start);
} else {
    sreq.params.set(CommonParams.START, "0");
}
if (rb.shards_rows > -1) {
    // if the client set shards.rows set this explicity
    sreq.params.set(CommonParams.ROWS, rb.shards_rows);
} else {
    sreq.params.set(CommonParams.ROWS, rb.getSortSpec().getOffset()
            + rb.getSortSpec().getCount());
}
```
打印日志rb.shards_start与rb.shards_rows都为-1,于是start变为0,row变成30,这是正确的,那么关键点就是要找出start和rows何时变成20与10，跟踪程序找不到原因。看后台日志,发现初始化每次都会执行两次,然后想到分布式，才渐渐明白问题的原因.

在一次分布式查询中,solr的leader会接受请求，然后对请求进行解析，之后重新构建请求，将新的请求发给各个Shard,Shard做非分布式查询之后,将结果发给leader,之后leader汇总各个Shard的响应,进行最后的处理(如做offset等),问题是leader和Shard都是同一份代码,而且初始化部分每个Shard接收leader的请求后都要执行,于是start和rows又被重新设置了.在上面的例子中,start和rows在Shard中分别被设置成20和10了,只会Shard做非分布式查询,这样Shard只会返回10条数据给leader，这显然不是想要的.

之后发现,在leader构建的新的请求中,会添加isShard=true参数,于是可以修改代码如下:
``` 
boolean isShard = req.getParams().getBool(ShardParams.IS_SHARD, false);
if ( pidStr != null && !isShard) { //分布式时，只有leader才需要执行这里
```
之后结果就是正确的。到这里，才有点明白分布式程序，真不好写.

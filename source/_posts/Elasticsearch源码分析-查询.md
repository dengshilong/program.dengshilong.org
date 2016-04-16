title: Elasticsearch源码分析-查询
date: 2016-04-16 16:04:59
tags: Elasticsearch
categories: 搜索引擎
---
在[Elasticsearch源码分析-启动](http://program.dengshilong.org/2016/04/15/Elasticsearch源码分析-启动/)里简单了解Elasticsearch的启动过程，这里来看看查询过程。

## 接收请求
从启动篇里知道HttpRequestHandler，进入这个类查看，看到messageReceived, 进入NettyHttpRequest, 看到String uri = request.getUri(); 看到这里没有日志输出，一直纳闷为什么Elasticsearch没有请求url输出，于是加上日志
```
try {
    logger.info("query uri {}", URLDecoder.decode(uri, "UTF-8"));
} catch (java.io.UnsupportedEncodingException e) {
    logger.info("query uri {}", uri);
}
```
之后日志里就有请求的uri了。看到RestUtils.decodeQueryString(uri, pathEndPos + 1, params), 知道请求参数是在这里完成解析。

查看serverTransport.dispatchRequest,进入httpServerAdapter.dispatchRequest(request, channel)，这里要知道httpServerAdapter的具体对象，查看
```
public void httpServerAdapter(HttpServerAdapter httpServerAdapter) {
    this.httpServerAdapter = httpServerAdapter;
}
```
被哪个函数调用，跳到HttpServer.java, 打开server.internalDispatchRequest(request, channel); 之后到了restController.dispatchRequest(request, channel);
    
最终请求的处理由restController.dispatchRequest(request, channel);完成

## 请求处理
进入RestController的dispatchRequest方法, 进入executeHandler方法, 在getHandler(request)里，根据不同的请求方法，返回不同的handler,然后调用handler里的handleRequest方法处理请求，这里以GET方法为例。

对于不同的动作，都可以使用GET方法，如curl -XGET /index/type/id, curl -XGET /index/type/_search, 这里以/index/type/_search这查询为例。

在RestSearchAction.java里，有语句`controller.registerHandler(GET, "/{index}/{type}/_search", this);`, 所以执行curl -XGET /index/type/_search时，得到的handler就是RestSearchAction, 并执行这个类里的handleRequest方法。

进入RestSearchAction.java里的handleRequest方法，先是执行RestSearchAction.parseSearchRequest(searchRequest, request, parseFieldMatcher, null)，这个方法主要对查询参数进行设置，之后调用client.search(searchRequest, new RestStatusToXContentListener<SearchResponse>(channel))进行查询。

### client类型
现在要弄清楚client的具体类型, 在Node初始化里，有modules.add(new NodeClientModule())这句，打开查看，有bind(Client.class).to(NodeClient.class).asEagerSingleton()，所以这里的client具体类型是NodeClient, 而NodeClent继承自AbstractClient,

然后看查询调用过程client.search ->client.execute->client.doExecute->transportAction.execute, 最终还是由transportAction来完成实际的查询

值得注意的一点是client. execute是execute(SearchAction.INSTANCE, request, listener);

### transportAction类型
在Node初始化时，有modules.add(new ActionModule(false))，进入ActionModule.java查看，有registerAction(SearchAction.INSTANCE, TransportSearchAction.class);所以transportAction是TransportSearchAction类型。

### 具体执行
transportAction.execute最终会调用transportAction.doExecute, 这里是进入TransportSearchAction.java的doExecute,这里会对search_type进行判断

对于search_type, 是由RestSearchAction.java里的searchRequest.searchType(searchType)语句设定，默认是SearchType.DEFAULT, 也就是SearchType.QUERY_THEN_FETCH

### query阶段
由此新建了一个SearchQueryThenFetchAsyncAction实例，之后searchAsyncAction.start();开始查询。在父类AbstractSearchAsyncAction的start()函数里,
```
for (final ShardIterator shardIt : shardsIts) {
    shardIndex++;
    final ShardRouting shard = shardIt.nextOrNull();
    if (shard != null) {
        performFirstPhase(shardIndex, shardIt, shard);
    } else {
        // really, no shards active in this group                 
        onFirstPhaseResult(shardIndex, null, null, shardIt, new NoShardAvailableActionException(shardIt.shardId()));
    }
}
```
对每一个shard调用performFirstPhase,

查看performFirstPhase, 最终会调用sendExecuteFirstPhase,并添加了ActionListener, 如果成功则执行onResponse里的onFirstPhaseResult, 在onFirstPhaseResult里有个判断, if (xTotalOps == expectedTotalOps)，当所有shard都执行完后，执行innerMoveToSecondPhase, 最终执行moveToSecondPhase

### fetch阶段
在moveToSecondPhase里, sortedShardList = searchPhaseController.sortDocs(useScroll, firstResults)对第一阶段的结果进行合并，之后对每个shard里入选到topN的doc进行fetch,即执行executeFetch(entry.index, queryResult.shardTarget(), counter, fetchSearchRequest, node)，

在executeFetch里, 
```
if (counter.decrementAndGet() == 0) {
    finishHim();
}
```
当所有需要执行的shard都结束后，执行finishHim()，标志着查询结束。

在finishHim里，
```
final InternalSearchResponse internalResponse = searchPhaseController.merge(sortedShardList, firstResults,fetchResults, request);
```
对fetch阶段Shard返回的结果进行合并.
```
listener.onResponse(new SearchResponse(internalResponse, scrollId, expectedSuccessfulOps,successfulOps.get(), buildTookInMillis(), buildShardFailures()))
```
设置返回的SearchResponse对象.

## 请求结果返回
在TransportAction调用execute时，有添加Actionlistener, 
```
public void onResponse(Response response) {
    taskManager.unregister(task);
    listener.onResponse(response);
}
```
这里的Response就是上面返回的SearchResponse, 而listener可以在RestSearchAction中找到, 是RestStatusToXContentListener<SearchResponse>(channel).

RestStatusToXContentListener继承RestResponseListener, RestResponseListener继承RestActionListener, 最终onResponse方法会调用RestStatusToXContentListener中的buildResponse, 也就调用了SearchResponse中的toXContent方法。

到此，大致了解Elasticsearch的查询过程。目前，我修改JSON返回格式，就是修改SearchResponse的toXContent方法。

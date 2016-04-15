title: Elasticsearch源码分析-启动
date: 2016-04-15 20:06:06
tags: 
    - Elasticsearch
categories:
    - 搜索引擎
---
## 前言
刚开始使用Elasticsearch时，我只需要修改Elasticsearch的_search这个查询的返回格式，使之与django-rest-framework的返回结果一致，凭着修改Solr的JSONResponseWriter返回结果的经验，在没有研究Elasticsearch源码的情况下，很快找到了org.elasticsearch.action.search.SearchResponse类，并进行修改，虽然遇到一些问题，但最终还是达到了目的。最近需要修改[top hits aggregations](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-top-hits-aggregation.html)的返回结果，于是开始看源码。
## 准备工作
### 修改日志
* 修改config下的logging.yml, 将所有INFO替换为DEBUG，
* 将`conversionPattern: "[%d{ISO8601}][%-5p][%-25c]: %.10000m%n"` 改为`conversionPattern: "[%d{ISO8601}][%-5p][%l]: %.10000m%n"`以便查看到更多的日志，这里建议生产环境中也这样设置，这个更容易查找错误
### 查看程序入口
查看bin目录下的启动脚本elasticsearch, 知道程序入口是org.elasticsearch.bootstrap.Elasticsearch
## 深入代码
* 进入Bootstrap.java的init方法,    `Environment environment = initialSettings(foreground);`加载环境配置,
* 进入`INSTANCE.setup(true, settings, environment);`，`JarHell.checkJarHell();`完成jar hell检查, 跟踪`node = nodeBuilder.build();`，发现是这里新建Node，并完成初始化
### Node初始化
* 在Node的构造函数里,`nodeEnvironment = new NodeEnvironment(this.settings, this.environment);`完成Node环境初始化,
* `final ThreadPool threadPool = new ThreadPool(settings);`完成线程池初始化，进入ThreadPool可以看到对于不同任务会建立不同的线程池。
* Elasticsearch使用Guice作为依赖注入容器，这在 `ModulesBuilder modules = new ModulesBuilder();`里有所体现，这里主要关注RestModule, TransportModule,HttpServerMoudle的配置。
* 进入RestModule.java之后进入RestActionModule.java,可以看到配置了许多RestAction,
* 进入TransportModule.java, 可以看到NettyTransport,
* 进入HttpServerModule.java,可以看到使用NettyHttpServerTransport.
### Node启动
进入INSTANCE.start(),之后进入node.start(), 可以看到得到很多实例，
* 对于RestController, 进入之后可以看到在registerHandler函数里对不同的request method绑定了不同的handler
* 对于TransportServer, 默认绑定到9300端口, 这个用来做集群节点间通信
* 对于HttpServerTransport,在配置里使用NettyHttpServerTransport, 所以这里实际上是得到NettyHttpServerTransport实例, 默认绑定到9200端口, 这个用来处理http请求
## NettyHttpServerTransport
进入NettyHttpServerTransport, 在doStart()函数里，看到serverBoostrap是Netty的ServerBootstrap实例,看到`serverBootstrap.setPipelineFactory(configureServerChannelPipelineFactory());`, 查看configureServerChannelPipelineFactory, 知道requestHandler是HttpRequestHandler

这样，差不多就完成了Elasticsearch的启动。

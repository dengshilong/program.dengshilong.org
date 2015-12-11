title: Solr分布式group查询过程
tags:
  - group查询
  - solr
  - 分布式
id: 926
categories:
  - 搜索引擎
date: 2014-10-18 11:45:09
---

最近因为需要在分布式group查询时自定义自己的排序，因为在许多应用中都需要定义针对应用的排序规则。例如在用户名时，需要针对name,添加最匹配原则最左侧优先,最短优先等排序规则。而要使用这些规则， 一个前提条件是，先要拿到这个字段的值。可是在Solr提供的api中，无法定义这样精细的规则，所以必须修改代码才能支持.

在此之前，要了解分布式group查询的过程.当进行分布式group查询时,从QueryComponent中，可以知道,leader会向shard发送三次请求,分别对应三个阶段 ResponseBuilder.STAGE_TOP_GROUPS，ResponseBuilder.STAGE_EXECUTE_QUERY，ResponseBuilder.STAGE_GET_FIELDS三个阶段。

第一个阶段也可称为firstPhase,主要是得到字段的分组信息，也就是得到字段有哪些分组,请求的构造在 SearchGroupsRequestFactory中.在shard中，对这次请求作出响应是在QueryComponent中的process函数 内，if (params.getBool(GroupParams.GROUP_DISTRIBUTED_FIRST, false)) 中完成的，查询得到的结果由SearchGroupsResultTransformer的transform进行转换。对于shard返回的结 果，leader在SearchGroupShardResponseProcessor中进行处理.

第二个阶段也可称为secondPhase,这个阶段主要是得到每个分组内的文档id,在这个阶段,leader会将上一阶段得到的分组 信息发给shard,请求的构造在TopGroupsShardRequestFactory中.在shard中,对这次请求作出响应是在 QueryComponent中的process函数内，else if (params.getBool(GroupParams.GROUP_DISTRIBUTED_SECOND, false))中完成，查询得到的结果由TopGroupsResultTransformer的transform函数进行转换。对于shard返回的 结果,leader在TopGroupsShardResponseProcessor中进行处理

第三个阶段主要是得到文档的字段信息，在这个阶段，leader会将最终结果中的文档id发送给shard,请求的构造在 StoredFieldsShardRequestFactory中.在shard中，对这次请求作出响应是在QueryComponent中的 process函数内,String ids = params.get(ShardParams.IDS);语句后的if (ids != null)中。对于shard返回的结果,leader是在StoredFieldsShardResponseProcessor中. 

分布式group查询的过程差不多就这样，以后再介绍如何定义自己的排序。
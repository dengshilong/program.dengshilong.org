title: Solr分布式请求stage理解
tags:
  - solr
  - stage
  - 分布式
id: 940
categories:
  - 搜索引擎
date: 2014-10-20 20:52:51
---

从QueryComponent可以知道，一个分布式solr请求从发起请求到对响应的结果进行处理会经历许多的stage.

对于分布式普通请求，从private int regularDistributedProcess(ResponseBuilder rb)的实现中可以看到，会经历ResponseBuilder.STAGE_PARSE_QUERY,ResponseBuilder.STAGE_EXECUTE_QUERY,ResponseBuilder.STAGE_GET_FIELDS,ResponseBuilder.STAGE_DONE等stage。从private void handleRegularResponses(ResponseBuilder rb, ShardRequest sreq)，分布式普通请求有ShardRequest.PURPOSE_GET_TOP_IDS，ShardRequest.PURPOSE_GET_FIELDS两次响应

对于分布式group请求,从private int groupedDistributedProcess(ResponseBuilder rb)的实现中可以看到，则会经历ResponseBuilder.STAGE_PARSE_QUERY，ResponseBuilder.STAGE_TOP_GROUPS，ResponseBuilder.STAGE_EXECUTE_QUERY，ResponseBuilder.STAGE_GET_FIELDS，ResponseBuilder.STAGE_DONE等stage。从private void handleGroupedResponses(ResponseBuilder rb, ShardRequest sreq)可以看到，分布式group请求有ShardRequest.PURPOSE_GET_TOP_GROUPS,ShardRequest.PURPOSE_GET_TOP_IDS,ShardRequest.PURPOSE_GET_FIELDS三次响应.

对于不同的请求和响应，有相应的类或者方法来实现。当然也可以自己实现相应的类或者方法来处理。即便是QueryComponent也可以自己定义，只需要实现相应的接口即可。

对于private int regularDistributedProcess(ResponseBuilder rb),一个可能的实现是：
``` java
 private int regularDistributedProcess(ResponseBuilder rb) {
        ComponentDistributedStage cdStage = stages.getCDStage(rb.stage);
        int nextState = ResponseBuilder.STAGE_DONE;
        if (cdStage != null) {
            cdStage.distributedProcess(rb, this);
            if (stages.containsNextState(rb.stage))
                nextState = stages.getNextState(rb.stage);
        }
        return nextState;
    }
```
这里stages是一个Map,保存相应stage的实现类，父类型为ComponentDistributedStage。具体实现一个stage时，实现相应的接口即可。
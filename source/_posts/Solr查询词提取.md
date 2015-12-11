title: Solr查询词提取
tags:
  - awk
  - grep
  - sort
  - uniq
id: 972
categories:
  - shell
date: 2014-12-04 21:28:02
---

最近因为负责一个小功能，所以想尽力做好它。于是对会经常看看用户的查询，看看这些查询的结果是否满足需要，于是需要对这些查询词进行提取。本来还想用Python来写的，后来想想shell才是做这事的最佳方法，于是先从grep开始。

solr的日志中,query都是跟在‘q=’后面，且参数间用&隔开，于是执行如下命令，
grep -o 'q=.*\&' solr.log
得到如下结果
q=磐安&macro.skip=0&qt=macro&wt=json&
q=磐安+财政&macro.skip=0&qt=macro&wt=json&
q=保定+财政&macro.skip=0&qt=macro&wt=json&
q=磐安+财政&macro.skip=0&qt=macro&wt=json&
q=财政+长春&macro.skip=0&qt=macro&wt=json&
q=财政+长沙&macro.skip=0&qt=macro&wt=json&
q=存款收入&macro.skip=0&qt=macro&wt=json&
q=存款收入&qt=macro&wt=json&macro.groupOffset=0&macro.groupNames=利率走势&
q=存款收入&qt=macro&wt=json&macro.groupOffset=0&macro.groupNames=行业经济&
q=存款收入&qt=macro&wt=json&macro.groupOffset=0&macro.groupNames=区域宏观&
q=存款收入&qt=macro&wt=json&macro.groupOffset=0&macro.groupNames=中国宏观&

之后就是截取query部分，这时awk就派上用场了。先用&分割，得到第一段，之后用=分割，得到第二段
grep -o 'q=.*\&' solr.log | grep -v 'module2:' | grep -v 'solrconfig.xml' | awk -F '&' '{print $1}' | awk -F '=' '{print $2}'
结果如下：
磐安
磐安+财政
保定+财政
磐安+财政
财政+长春
财政+长沙
存款收入
存款收入
存款收入
存款收入
存款收入

之后想统计每个查询词的次数，此时先用sort排序，之后用uniq -c来统计，
grep -o 'q=.*\&' solr.log | grep -v 'module2:' | grep -v 'solrconfig.xml' | awk -F '&' '{print $1}' | awk -F '=' '{print $2}'  |sort | uniq -c
结果如下：
1 保定+财政
5 存款收入
1 磐安
2 磐安+财政
1 财政+长春
1 财政+长沙

而我希望按查询次数从高到低排列，于是再用sort -rn
grep -o 'q=.*\&' solr.log | grep -v 'module2:' | grep -v 'solrconfig.xml' | awk -F '&' '{print $1}' | awk -F '=' '{print $2}'  |sort | uniq -c | sort -rn
结果如下：
5 存款收入
2 磐安+财政 
1 财政+长沙
1 财政+长春
1 磐安
1 保定+财政

一行代码搞定。一句话，管道实在是太方便了，linux也是如此。
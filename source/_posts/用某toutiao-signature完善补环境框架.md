title: 用某toutiao_signature完善补环境框架
date: 2022-12-12 20:39:34
tags:
    - js
    - 补环境
    - vmp
    - rs
categories:
---
在搞定rs4后，补环境技术成了我手中的锤子，我直接化身西北锤王，见到一个网站就想用补环境去锤一下，很快就搞好了rs5，接下来就要搞定rs6, 但因为rs6是vmp, 所以在这之前，得先搞点简单的vmp热热身，toutiao是个不错的选择。

关于vmp，可以看看Nanda的[VM防护介绍及企鹅滑块分析](https://mp.weixin.qq.com/s/C8gB-D6EUliPXoMgjk0Bag), 关于vmp打日志，可以看看卷木木的[新版某数分析思路](https://mp.weixin.qq.com/s/NmaNND6Up1k_xnovtexgCg)

完成rs5后，除了dom树操作，环境已经相对比较完善了，再来搞toutiao,  就会发现简单很多。相比较rs5, toutiao主要增加了对WebGL对象的校验，以及Plugins的校验。其中WebGL缺啥补啥就完事了，而Plugins的补充就麻烦很多，好在肝总大佬已经有现成的代码，直接拿来用就行了，真是省心又省力。

打上日志，toutiao的vmp就只执行了3000多次，而rs6执行了2万多次才生成cookies，规模上的差距还是很大的，但道理是相通的。搞定toutiao后再来搞rs6的vmp就轻松很多了，唯一困难的是rs6的dom树操作，要花些时间了，大佬们建议自己去实现dom树，还在想办法看看怎么实现中。

整体来说，toutiao用来做vmp入门是极好的，大佬们已经不是停留在补环境了，直接把加密算法都给还原了，真是人外有人。

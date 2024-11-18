title: Unidbg模拟执行简单版libsgmain.so
date: 2024-11-18 19:17:26
tags:
    - APP
    - 逆向
    - Unidbg
categories:
---
这几天一直在处理APP，遇到了libsgmain.so, 问了大佬和找资料后，基于Unidbg的demo跑通了，于是做个简单记录。

1. 代码里找不到核心加密接口和类，Frida里也hook不到(如ISecureSignatureComponent接口的实现类，JNICLibrary类)，是因为这些代码是动态注册的。如何解决看参考资料1
2. libsgmain.so是假so, 本质上是jar, 在jadx里打开就能看到核心加密类，真正的so文件也在这假so里，形如libsgmainso-*.so
3. doCommandNative是真正加密的方法，这个方法也用于初始化，至于初始化多少次，看so文件难度了， 我要处理的so相对简单，只有一次初始化，缺啥补啥完事。可以看参考资料2。
4. Unidbg真是大杀器，so加密小白福音。


参考资料

1. 奋飞佬的[某A系电商App x-sign签名分析](https://www.jianshu.com/p/e4395b49094a)
2. 意识存在感的[阿里系某电影票务APP加密参数还原-Unidbg篇](https://blog.csdn.net/weixin_44084602/article/details/126923221)

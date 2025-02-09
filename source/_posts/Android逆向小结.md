title: Android逆向小结
date: 2025-02-09 17:47:13
tags:
    - APP
    - 逆向
categories:
---
24年下半年算是比较密集搞APP的一段时间，不得不说，Android逆向要学的东西比Web真是多多了。Web拿着浏览器就开始调试了，Android得学习一堆工具。Android逆向要解决的问题也比Web多多了，连抓包都是个问题。每次都是直接上强度，20年刚来做爬虫时直接就开搞rs, 24年Android逆向时直接就是企业级, 像libsgmain.so, libmpaas_crypto.so这种。好的一点是遇到的难点都是加密，没有风控，要不然就更头疼了。

这里列举下Andorid逆向遇到的问题，root检测，Frida反调试(因为我主要是用Frida分析，用Xposed的话也会遇到Xposed反调试), SSL pinning机制，加固壳, so加密。真是一步一个坑，举步维艰。还好有好多开源的工具, 有大佬们的星球可以学习，要不然真的累麻了。下面记录下每一步都是如何解决的，以供参考。


# root检测

最开始是用Magisk里的Shamiko模块，但发现这个过不去一些检测，后面了解到还有kernelSU和APatch，因为手上都是一些便宜手机，带不动kernelSU，就用APatch, 能解决问题。

# Frida反调试

大都是通过hook pthread_create解决，搞不定就请大佬出山。这里重点推荐霜哥的星球。

# SSL pinning机制
之前APP抓包进阶里写过，用DroidSSLUnpinning完事。

# 加固壳
开源的Fart，Fartext，MikRom试试，搞不定的话只好请小黄鱼大神解决了

# so加密
用Unidbg一把梭，Unidbg搞不定的话，只能慢慢分析so了，我也不会了。这里推荐白龙的星球，写的真的细。

根据https://www.52pojie.cn/thread-1244902-1-1.html 这篇文章写的，现在停留在基础技能的阶段，后续有时间再学习了。遇到问题多去Github, 看雪，吾爱破解找找。

# 参考资料
* 霜哥 https://github.com/xyxdaily/lessons
* 白龙 https://blog.csdn.net/qq_38851536/category_11102404.html

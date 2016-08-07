title: 再谈Supervisor管理进程
date: 2016-08-07 11:11:56
tags:
    - Supervisor
categories:
    - 软件安装
---
在[用Supervisor管理进程](http://program.dengshilong.org/2016/07/31/%E7%94%A8Supervisor%E7%AE%A1%E7%90%86%E8%BF%9B%E7%A8%8B/)里说过，当supervisor挂了之后，它管理的进程就给了init进程，之后supervisor再次启动，端口已经被绑定了，怎么破？目前还没有找到解决的办法。现在继续说说这个问题。

这里说当supervisor挂了之后，它管理的进程就给了init进程，这并不完全对。这里其实是我主动用kill命令把supervisor杀掉，而且是用kill -9, 此时supervisor来不及将被杀的信息告诉管理的进程就死了，于是管理的进程变成了孤儿进程。当使用kill -15杀死supervisor时，它管理的进程也会一起挂掉，这样进程所占的资源也来得及释放。supervisor下次就可以正常启动。

### 一篇错误的博客
在[linux 后台进程管理利器supervisor](http://www.cnblogs.com/youxin/p/4147384.html)里看到

> 不带参数运行supervisord是以daemon方式运行
当supervisord以非daemon方式运行时，杀掉supervisord后，被监控的进程也退出了。
而以daemon方式运行，杀掉supervisord对被监控进程无影响

然后我在博客里找什么是带参数和不带参数

>supervisord (以daemon方式启动)
或 supervisord -c /etc/supervisord.conf （非daemon）

后来看了supervisor的官方文档，知道supervisor是否以daemon方式启动，是在supervisord.conf的supervisord项里配置的。当配置了nodaemon=true时，就会以非daemon方式启动，而不是根据带参数和不带参数决定的。

而被监控的进程是否一起死掉，也是更加supervisor被杀的方式决定的。从这方面看，这篇博客真是错误连篇。

### 一些需要注意的地方
* autorestart=true
在program配置项里，最好加上这个配置项，让监控的程序在关闭后自动重启。我遇到过一个问题是，用kill -15把监控的进程杀掉，之后程序没有自动重启。原因是它的退出码是0, 而exitcodes的默认配置是0,2 此时程序不会自动重启。因为exitcodes里配置的是`The list of “expected” exit codes for this program used with autorestart`, 而autorestart默认配置是unexpected。

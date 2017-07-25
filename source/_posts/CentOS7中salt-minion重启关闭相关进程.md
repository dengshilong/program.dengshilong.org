title: CentOS7中salt-minion重启关闭相关进程
date: 2017-07-25 22:00:33
tags:
    - Salt
    - systemd
categories:
---
随着机器数量增多，单个Salt master已经无法满足性能需求，于是需要采用多master, 多syndic结构，于是需要升级Salt Minion。升级过程中出现了一些问题。

在升级Salt inion的时候，需要关闭当前的Salt minion,发现以前通过Salt启动的一些进程，如redis等等，也跟着关闭了，这是个问题。

查找之后，在Salt上也提到这个问题，[salt-minion restart causes all spawned daemons to die on centos7 (systemd)](https://github.com/saltstack/salt/issues/22993)，主要原因是Systemd里, [杀死进程](https://www.freedesktop.org/software/systemd/man/systemd.kill.html)的默认方式是control-group，也就是同一个组下主进程被杀死，其它进程都会被杀死。而通过Salt启动的那些服务与Salt是同一个组，Salt是主进程。

解决办法是更改salt-minion.service的KillMode为process

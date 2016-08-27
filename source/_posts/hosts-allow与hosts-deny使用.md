title: hosts.allow与hosts.deny使用
date: 2016-08-27 11:13:20
tags:
    - Linux
categories:
---
服务器上老是有人尝试破解root用户的SSH登录密码，要想办法解决。一个办法是屏蔽ip.

在/etc目录下存在hosts.allow和hosts.deny, 看名字就知道它们的意义。

* hosts.allow指的是允许登录的ip
* hosts.deny指的是不允许登录的ip
* 两个文件配置后自动生效，不要重启什么服务，因为监控这两个文件的服务会自动加载两个文件里的内容
* 添加了屏蔽ip后，在/var/log/secure里就可以看到效果
如在/etc/hosts.allow里添加
```
sshd:101.71.255.*
```
则是允许101.71.255.*等ip地址SSH登录

在/etc/hosts.deny里添加
```
sshd:116.31.116.*
```
则是禁止116.31.116.*等ip地址SSH登录。

hosts.allow和hosts.deny里配置的地址如果出现重复，优先使用hosts.allow, 也就是允许该地址SSH登录。

在/etc/hosts.deny里还可以添加
```
sshd:all
```
此时，只有hosts.allow里配置的地址才允许SSH登录。在我看来, hosts.allow配置只有当hosts.deny配置了`sshd:all`才有意义。

其实解决暴力破解root用户密码的最好办法是禁止root用户SSH登录，而用普通用户登录，登录之后切换到root用户。

兼任运维以来，数据库出问题，文件系统出问题，也是运气差。目前来看，还有很多地方需要完善的，慢慢来吧。

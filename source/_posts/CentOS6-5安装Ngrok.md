title: CentOS6.5安装Ngrok
date: 2016-08-01 20:39:30
tags:
    - Ngrok
    - CentOS
categories:
    - 软件安装
---
一直卡在gopkg.in/inconshreveable/go-update.v0, 
想在CentOS6.5上安装Ngrok, 按照[搭建 ngrok 服务实现内网穿透](https://imququ.com/post/self-hosted-ngrokd.html)上的步骤安装。遇到问题，记录一下。

* no package golang available.

参考[CentOS-6.x下搭建golang环境的三种方式](http://www.sudops.com/cengos-install-golang-env-in-three-ways.html)

* no package build-essential available

参考[CentOS Install Build Essentials](https://linuxmoz.com/centos-install-build-essentials/)

* 卡在gopkg.in/inconshreveable/go-update.v0  (download)

参考[ngrok服务安装笔记](http://xiayun.blog.51cto.com/2344243/1705259), 知道是git版本太旧。更新之后就可以编译成功

在CentOS6.5上如何更新git, 可参考[CentOS6.5升级git](http://program.dengshilong.org/2016/08/01/CentOS6-5%E5%8D%87%E7%BA%A7git/)

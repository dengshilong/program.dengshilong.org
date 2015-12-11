title: Screen-会话管理工具
tags:
  - Screen
id: 901
categories:
  - 软件安装
date: 2014-09-04 22:47:33
---

工作一年后,才知道有Screen这个东西,太不应该了,也许真是环境影响人.

今天遇到问题,导师过来指导,看我的SecureCRT开着很多个会话,没有用Screen,于是提醒可以用这个.之前在公司的wiki上看到过介绍,本以为就是SecureCRT,原来是一个管理会话工具,有了它之后,就不需要再开很多个会话,然后关闭了.会话间的切换也可以很方便的用快捷键命令,而不是鼠标,因为鼠标极其影响效率.

用了公司一个员工的配置
hardstatus alwayslastline "%{=b}%{b}%-w%{.BW}%10>%n*%t%{-}%+w%< %=%{kG}%C%A, %Y-%m-%d"
screen -t local1 0 bash
screen -t local2 1 bash
screen -t local3 2 bash
screen -t local4 3 bash
screen -t local5 4 bash

select 0

vim ~/.screenrc,复制上面内容.之后就可以使用Screen了.一些常用命令如下:
c-a : Ctrl + a
screen -S name #开一个session
screen -S name -X quit #杀死session
c-a c #创建一个窗口
c-a n #next 窗口
c-a p #previous 窗口
c-a A #为窗口命名
c-a d #detach screen
c-a #跳转到number的窗口
screen -ls #查看窗口
screen -r name #连接一个session
screen -x name #共享session
<span style="color: #000000;">可以参考</span>[http://hunsefee.diandian.com/post/2010-10-28/7319178](http://hunsefee.diandian.com/post/2010-10-28/7319178)
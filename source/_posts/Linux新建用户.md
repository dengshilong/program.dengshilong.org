title: Linux新建用户
date: 2016-09-09 21:00:30
tags:
    - Linux
categories:
---
最近在DigitOcean买了VPS，又开始折腾主机。这次要记录下来。首先从新建用户开始。

### 新建用户
新增用户使用useradd命令，例如新增test用户，执行命令`useradd test`即可。新增用户后，要给用户设置密码，否则无法登录。

### 修改用户密码
设置密码使用passwd命令，例如给test用户设置密码，执行'passwd test'即可。


### 设置用户sudo不需要密码
每次安装软件都要切换到root用户比较麻烦，可以添加用户sudo时不需要密码。在/etc/sudoers文件里添加
`test ALL=(ALL) NOPASSWD: ALL`即可。

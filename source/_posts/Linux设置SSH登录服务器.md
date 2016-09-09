title: Linux设置SSH登录服务器
date: 2016-09-09 22:06:03
tags:
    - Linux
categories:
---
之前也设置过SSH登录，这次记下来吧。

### 生成公钥
使用ssh-keygen命令，例如执行`ssh-keygen -t rsa`即可

### 添加ssh key

在远程服务器的用户目录新建.ssh目录，新建authorized_keys文件，将本地上传的id_ras.pub里的内容添加到authorized_keys文件里。

这里需要注意.ssh和authorized_kesy权限，.ssh必须是700, 而authorized_keys文件只有文件拥有者有写权限。否则会提示`Authentication refused: bad ownership or modes for file /home/dengsl/.ssh/authorized_keys`错误。所以authorized_keys的权限设置必须为600, 640等等。

从阮一峰的博客里看到一条命令，但其实这条命令里存在错误，修改之后如下
```
ssh user@host 'mkdir -p .ssh && chmod 700 .ssh && touch .ssh/authorized_keys && chmod 600 .ssh/authorized_keys && cat >> .ssh/authorized_keys' < ~/.ssh/id_rsa.pub
```
之后会提示输入密码，之后就可以不需要密码登录了。


### 禁止root用户登录
修改/etc/ssh/sshd_config文件，在#PermitRootLogin yes后面添加`PermitRootLogin no`即可。之后重启sshd服务`service sshd restart`使修改的配置生效

参考资料
* [SSH原理与运用（一）：远程登录](http://www.ruanyifeng.com/blog/2011/12/ssh_remote_login.html)
* [linux ssh 使用深度解析（key登录详解）](http://blog.lizhigang.net/archives/249)

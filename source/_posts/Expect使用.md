title: Expect使用
date: 2017-09-22 20:07:19
tags:
    - Expect
    - Shell
categories:
---
需要通过带外卡获取服务器的业务网卡，本来想使用 IPMI 获取的，但惠普的服务器不支持。好在可以通过 SSH 的方式获取，SSH 登录后执行 `show /system1/network1/Integrated_Nics` 命令即可。

但是不知道什么原因，使用 Python 的 paramiko 模块无法登录带外的 SSH, 于是只好用其它办法，同事建议用 [Expect](http://expect.sourceforge.net/) 来实现自动登录, 于是编写了如下脚本，替换上相应的主机，用户，密码即可

```
#!/usr/bin/expect -f
set ip 10.48.2.3
set password test123
set timeout 5
spawn ssh administrator@$ip
expect {
    "*yes/no" { send "yes\r"; exp_continue}
    "*password:" { send "$password\r" }
}
expect "*hpiLO*"
send "show /system1/network1/Integrated_Nics\r"
send  "exit\r"
expect eof
```

## 参考资料
* [linux expect自动登录ssh,ftp](http://blog.51yip.com/linux/1462.html)
* [linux 安装 expect tcl](http://blog.csdn.net/supingemail/article/details/46680539)

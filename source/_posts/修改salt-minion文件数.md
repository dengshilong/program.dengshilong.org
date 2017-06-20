title: 修改salt-minion文件数
date: 2017-06-20 10:12:34
tags:
    - Salt
categories:
---
使用salt-minion时，会遇到文件数不够的问题。一个常见的误区是认为修改/etc/security/limits.conf即可，后来发现这是不对的。man pam_limits就会发现/etc/security/limits.conf主要作用于user-session的情况，如sshd, login, su等等。而对于使用sysvinit和systemd启动的服务，/etc/security/limits.conf是不起作用的，此时可以在相应服务的启动配置里修改文件数配置。

对于salt-minion文件数的修改需要根据系统版本而定。

# CentOS 7

修改/usr/lib/systemd/system/salt-minion.service文件，修改其中的LimitNOFILE配置
之后重启 salt-minion
* systemctl daemon-reload
* systemctl restart salt-minion.service

# CentOS 6

修改/etc/init.d/salt-minion启动脚本
添加文件数ulimit配置。例如设置最大100000，可以在启动脚本前面添加ulimit -HSn 100000，之后重启 salt-minion
* service salt-minion restart

# 参考资料:

* https://onebitbug.me/2014/06/23/setting-limit-in-linux/
* http://www.cnblogs.com/Richardzhu/p/5860457.html

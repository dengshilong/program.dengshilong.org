title: 用Supervisor管理进程
date: 2016-07-31 16:34:10
tags:
    - Supervisor
categories:
    - 软件安装
---
以前就用过[Supervisor](http://supervisord.org/)，但没有细看，这次认真的使用了之后，还是发现了一些问题。

- 如何让Supervisor成为服务

如果是通过`pip install supervisor`这种方式安装的Supervisor, 如何让Supervisor成为系统的一种服务，让系统开机时自动启动，在[这里](https://github.com/Supervisor/initscripts)给出了一些例子，然而，我的系统是Centos 6.5, 这些例子没有包括。于是通过yum install supervisor的方式安装，得到了/etc/init.d/supervisord下的服务脚本. 之后把通过yum安装得到的/usr/bin/supervisord和/usr/bin/supervisorctl替换成pip安装得到的/usr/local/bin/supervisord和/usr/local/bin/supervisorctl

```
#!/bin/bash
#
# supervisord   This scripts turns supervisord on
#
# Author:       Mike McGrath <mmcgrath@redhat.com> (based off yumupdatesd)
#
# chkconfig:    - 95 04
#
# description:  supervisor is a process control utility.  It has a web based
#               xmlrpc interface as well as a few other nifty features.
# processname:  supervisord
# config: /etc/supervisord.conf
# pidfile: /var/run/supervisord.pid
#

# source function library
. /etc/rc.d/init.d/functions

RETVAL=0

start() {
    echo -n $"Starting supervisord: "
    daemon supervisord
    RETVAL=$?
    echo
    [ $RETVAL -eq 0 ] && touch /var/lock/subsys/supervisord
}

stop() {
    echo -n $"Stopping supervisord: "
    killproc supervisord
    echo
    [ $RETVAL -eq 0 ] && rm -f /var/lock/subsys/supervisord
}

restart() {
    stop
    start
}

case "$1" in
  start)
    start
    ;;
stop)
    stop
    ;;
  restart|force-reload|reload)
    restart
    ;;
  condrestart)
    [ -f /var/lock/subsys/supervisord ] && restart
    ;;
  status)
    status supervisord
    RETVAL=$?
    ;;
  *)
    echo $"Usage: $0 {start|stop|status|restart|reload|force-reload|condrestart}"
    exit 1
esac

exit $RETVAL
```

- Supervisor无法管理daemon进程

在启动Shadowsock的时候，加了-d参数
`/usr/local/bin/ssserver -p 443 -k password --user nobody -d start`, 也就是让它成为daemon进程，于是Supervisor就无法管理了。所以之后把这个参数去掉。

- 当supervisor挂了之后，它管理的进程就给了init进程，之后supervisor再次启动，端口已经被绑定了，怎么破？目前还没有找到解决的办法。

参考资料
* [使用 supervisor 管理进程](http://liyangliang.me/posts/2015/06/using-supervisor/)

* [监控进程](http://huoding.com/2015/02/11/419)

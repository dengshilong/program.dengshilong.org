title: Supervisor之stopasgroup
date: 2016-09-02 16:58:16
tags:
    - Supervisor
    - Python
categories:
    - Python
---
在使用Supervisor监控Django项目时，在我的自己的站点设置里，没有加上stopasgroup＝true选项，也就是关闭子进程，子进程也会退出。所以在公司的配置里，也没有加上这个选项。

后来发现，如果不加，在有请求时，gunicorn不会关闭子进程，此时子进程会变成孤儿进程，导致了资源占用率很高。在配置项里加上后，程序就正常了。所以建议都加上这个配置。

参考资料
* http://supervisord.org/configuration.html#program-x-section-settings

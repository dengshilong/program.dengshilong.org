title: Supervisor重新加载配置
date: 2016-08-27 10:40:03
tags:
    - Supervisor
categories:
    - Python
---
当需要添加新的监控程序时，添加了配置后，需要重新加载，这样才能监控起来。此时`supervisorctl update`命令就派上用场了。

执行`supervisorctl update`命令后，添加的配置会加载到Supervisor里，这样就可以用Supervisor监控程序了。

发现program配置里有directory这个选项，目的是在启动程序时，让程序进入的目录。例如在使用gunicorn启动Django项目时，如果wsgi指定的路径使用/隔开，则会报`importerror import by filename is not supported`, 配置directory为wsgi所在的目录，问题就得到解决。

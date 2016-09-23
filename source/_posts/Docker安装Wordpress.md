title: Docker安装Wordpress
date: 2016-09-23 20:27:08
tags:
    - Docker
    - Wordpress
categories:
---
之前有几个站点是用Wordpress搭建的，准备迁移服务器后，需要安装Wordpress, 这次想用Docker来迁移。于是就在Docker中安装Wordpress. 看到Compose的文档里有一篇[Quickstart: Docker Compose and WordPress](https://docs.docker.com/compose/wordpress/), 于是使用Compose安装。

按照文档安装，报如下错误。
```
wordpress_mysql | 2016-09-22T09:34:33.723755Z 0 [ERROR] InnoDB: mmap(137428992 bytes) failed; errno 12
wordpress_mysql | 2016-09-22T09:34:33.723792Z 0 [ERROR] InnoDB: Cannot allocate memory for the buffer pool
```
发现是内存不够，因为已经安装了一个MySQL, 并且服务器内存只有512M, 于是内存吃紧, 只好放弃这种安装方法，直接连接现有的MySQL容器。

`docker pull wordpress`拉取最新版本的Wordpress后，执行命令后台启动Wordpress
```
docker run －d --name wordpress --link mysql:db -p 8000:80 -e WORDPRESS_DB_USER=root -e WORDPRESS_DB_NAME=wordpress -e WORDPRESS_DB_PASSWORD=password wordpress:latest
```
又发现CPU吃紧, 查看进程后发现loop0进程很占CPU，原来用的是Apache服务器，这就显得浪费了，我已经安装的Nginx了，而Wordpress镜像里还安装Apache。

得想想其它办法才好。当然如果内存足够，这样安装也没什么问题。

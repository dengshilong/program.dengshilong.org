title: Docker-Compose管理容器
date: 2016-11-20 20:12:24
tags:
    - Docker
    - Compose
categories:
---
[Docker-Compose](https://docs.docker.com/compose/)是用来定义和管理多个Docker容器的工具，用Python编写，前身是Fig.

使用Compose一般分为三步
* 定一应用的Dockerfile
* 编写docker-compose.yml, 在其中添加启动服务相关的配置
* 执行docker-compose up命令

目前[B7310实验室](http://b7310.dengshilong.org/)和[爱与生的烦恼](http://lovehate.cc/)就是使用Compose管理的。

环境配置放在[Github](https://github.com/dengshilong/Dockerfiles)上。

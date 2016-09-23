title: Docker镜像加速器设置
date: 2016-09-23 21:03:56
tags:
    - Docker
    - 加速器
categories:
---
国内访问Docker官网镜像很慢，需要修改镜像地址。阿里云的速度不错，注册之后就可以拿到专属加速器地址。

在[阿里云后台](https://cr.console.aliyun.com/#/accelerator)有说明，根据不同系统，版本号，有响应的设置

我的Ubuntu上
```
echo "DOCKER_OPTS=\"--registry-mirror=https://xxxxxx.mirror.aliyuncs.com\"" | sudo tee -a /etc/default/docker
sudo service docker restart
```
其中xxxxxx需要替换成专属加速器。

在我的Mac上，根据[Docker for Mac](https://docs.docker.com/docker-for-mac/), 参考[Preferences](https://docs.docker.com/docker-for-mac/#/preferences) 设置, 在Preference->Advanced->registry mirrors里添加专属加速器地址

参考资料:
* [Docker下使用daocloud/阿里云镜像加速](http://www.imike.me/2016/04/20/Docker%E4%B8%8B%E4%BD%BF%E7%94%A8%E9%95%9C%E5%83%8F%E5%8A%A0%E9%80%9F/)

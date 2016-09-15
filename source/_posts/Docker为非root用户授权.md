title: Docker为非root用户授权
date: 2016-09-15 09:53:03
tags:
    - Docker
    - Linux
categories:
---
因为启动docker服务器需要root权限，所以连接到docker服务器需要输入sudo, 即便设置了[sudo不需要输入密码](http://program.dengshilong.org/2016/09/09/Linux%E6%96%B0%E5%BB%BA%E7%94%A8%E6%88%B7/), 还是需要输入sudo, 可以通过增加docker组的方式来避免输入sudo.

### 增加一个docker组
sudo groupadd docker
### 将用户test加入docker组，用户test需要重新登录才能生效
sudo gpasswd -a test docker
### 重启docker服务
sudo service docker restart

此后执行docker命令就不需要加上sudo

参考资料:
* [Docker技术入门与实践](https://github.com/yeasy/docker_practice/)

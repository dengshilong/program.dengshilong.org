title: Docker安装MySQL
date: 2016-09-12 20:28:27
tags:
    - Docker
    - MySQL
categories:
    - 软件安装
---
准备慢慢的将香港VPS上的服务迁移到新的服务器，趁这个机会，学习使用Docker技术。首先安装MySQL
### 搜索MySQL镜像
使用docker search命令，docker search mysql
```
INDEX       NAME                                 DESCRIPTION                                     STARS     OFFICIAL   AUTOMATED
docker.io   docker.io/mysql                      MySQL is a widely used, open-source relati...   3021      [OK]
docker.io   docker.io/mysql/mysql-server         Optimized MySQL Server Docker images. Crea...   194                  [OK]
docker.io   docker.io/centurylink/mysql          Image containing mysql. Optimized to be li...   46                   [OK]
docker.io   docker.io/sameersbn/mysql                                                            36                   [OK]
```
### 下载MySQL镜像
使用docker pull命令，docker pull docker.io/mysql
### 启动MySQL镜像
使用docker run命令，执行docker run docker.io/mysql
提示
```
error: database is uninitialized and password option is not specified
  You need to specify one of MYSQL_ROOT_PASSWORD, MYSQL_ALLOW_EMPTY_PASSWORD and MYSQL_RANDOM_ROOT_PASSWORD
```
参考[How to connect to MySQL running on Docker from the host machine](http://stackoverflow.com/questions/33795923/how-to-connect-to-mysql-running-on-docker-from-the-host-machine)，执行`docker run --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=password -d docker.io/mysql`启动
### 访问MySQL容器
```
sudo docker exec -it mysql bash
mysql -uroot -ppassword
```
参考资料
* [Docker入门教程](http://www.docker.org.cn/book/docker/what-is-docker-16.html)

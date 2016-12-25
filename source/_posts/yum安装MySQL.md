title: yum安装MySQL
date: 2016-12-25 21:27:51
tags:
    - yum
    - MySQL
categories:
---
CentOS上安装MySQL, 使用yum安装很方便。

按照[A Quick Guide to Using the MySQL Yum Repository](http://dev.mysql.com/doc/mysql-yum-repo-quick-guide/en/)里的步骤即可。

### 配置镜像仓库
在[Download MySQL Yum Repository](http://dev.mysql.com/downloads/repo/yum/)下载仓库, 服务器是CentOS6, 于是下载mysql57-community-release-el6-9.noarch.rpm，之后执行`rpm -i mysql57-community-release-el6-9.noarch.rpm`

### 下载镜像
yum install mysql-community-server下载mysql

### 启动MySQL
service mysqld start

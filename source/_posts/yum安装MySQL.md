title: yum安装MySQL
date: 2016-12-25 21:27:51
tags:
    - yum
    - MySQL
categories:
---
CentOS上安装mysql, 使用yum安装很方便。

按照[A Quick Guide to Using the MySQL Yum Repository](http://dev.mysql.com/doc/mysql-yum-repo-quick-guide/en/)里的步骤即可。

### 配置镜像仓库
在[Download MySQL Yum Repository](http://dev.mysql.com/downloads/repo/yum/)下载仓库, 服务器是CentOS6, 于是下载mysql57-community-release-el6-9.noarch.rpm，之后执行`rpm -i mysql57-community-release-el6-9.noarch.rpm`

### 下载镜像
yum install mysql-community-server下载mysql

### 启动MySQL
service mysqld start
### 修改root用户密码
* 使用grep 'temporary password' /var/log/mysqld.log找到root用户密码，
* `mysql -uroot -p`登录,输入grep得到的密码
* 执行`ALTER USER 'root'@'localhost' IDENTIFIED BY 'MyNewPass4!';`修改root用户密码

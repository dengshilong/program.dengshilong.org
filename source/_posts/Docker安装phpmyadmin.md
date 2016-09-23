title: Docker安装phpmyadmin
date: 2016-09-23 19:59:26
tags:
    - Docker
    - phpmyadmin
categories:
---
phpmyadmin用来查看MySQL非常方便，决定给测试服务器上安装一个，这样开发人员就可以通过浏览器访问数据库，很方便。

查看[官方](https://hub.docker.com/r/phpmyadmin/phpmyadmin/)的说明文档，一直没弄懂要如何连接本地安装的MySQL, 好在测试环境的数据库是通过docker容器安装的，方便连接。

执行`docker pull phpmyadmin`拉取官方的镜像后，假设已经存在一个在运行的MySQL容器，名字叫mysql, 执行`docker run --name myadmin -d --link mysql:db -p 8000:80 -e PMA_USER=root -e PMA_PASSWORD=mysql123456 phpmyadmin/phpmyadmin`即可

其中--link是连接已经运行的mysql容器, db只是别名. 而PMA_USER和PMA_PASSWORD是连接mysql的用户名和密码, 这样开发人员在使用phpmyadmin时，就可以不用输入用户名和密码了，之后访问服务器的8000端口就可以访问MySQL数据库了，很方便。

参考资料:
* [Official phpMyAdmin Docker image](https://hub.docker.com/r/phpmyadmin/phpmyadmin/)

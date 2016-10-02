title: Nginx添加SSL支持
date: 2016-10-02 11:32:39
tags:
    - Nginx
    - HTTPS
categories:
---
需要给公司的域名添加HTTPS,决定先给自留地添加HTTPS支持，安装过程中遇到一些问题，记下来。
### libbrotli安装
安装libbrotli时，出现Makefile.am:5: Libtool library used but `LIBTOOL' is undefined，执行`yun install libtool`安装即可。
### /lib/lsb/init-functions: No such file or directory
执行yum provides '/lib/lsb/init-functions' 可以找到哪个包支持。
```
redhat-lsb-core-4.0-7.el6.centos.i686 : LSB base libraries support for CentOS
```
之后执行`yum install redhat-lsb-core-4.0-7.el6.centos.i686`即可
### 安装免费证书
本来想 Let's Encrypt, 但DNS解析出问题，想切换到外国的DNS，但考虑到公司的域名解析不能切换，所以继续找免费证书。最好找到[沃通](https://freessl.wosign.com)

参考资料
* [本博客 Nginx 配置之完整篇](https://imququ.com/post/my-nginx-conf.html)
* [CENTOS --- Installing Asterisk](https://www.centos.org/forums/viewtopic.php?t=52560)

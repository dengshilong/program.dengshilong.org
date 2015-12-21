title: 安装jdk源码
date: 2015-12-21 20:05:43
tags: jdk
categories: Java
---
要想提高Java水平，阅读jdk源码是很有必要的，所以要安装jdk源码。所幸安装过程很简单。

在jdk目录下，如(/home/long/jdk1.7.0_80)，有src.zip文件，这里保存了jdk源码。安装过程如下:

1. 进入jdk目录
cd /home/long/jdk1.7.0_80
2. 新建src子目录
mkdir src
3. 进入src子目录
cd src
4. 解压jdk源码
unzip ../src.zip

这样，在Eclipse中，按住ctrl键，单击类名，就可以看到源码了。

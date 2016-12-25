title: pip更换源
date: 2016-12-23 22:11:06
tags:
    - Python
    - pip
categories:
---
使用pip安装Python包时，因为要访问国外，会很慢，此时更换pip源可以加快速度。

在~/.pip/pip.conf文件里添加如下内容即可
```
[global]
index-url = https://pypi.douban.com/simple
```

参考资料
* [pip Configuration](https://pip.pypa.io/en/stable/user_guide/#configuration)
* [常用的开源镜像站推荐](http://smilejay.com/2015/11/mirrors-sites-for-open-source/)

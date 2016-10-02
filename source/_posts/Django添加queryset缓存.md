title: Django添加queryset缓存
date: 2016-10-02 22:46:59
tags:
    - Django
categories:
---
Django服务器的响应慢了, 想加上缓存。在网上查了之后，发现在queryset级别有3个选择。
* django-cache-machine
* johnny-cache
* django-cachalot

最后选择了[django-cachalot](https://github.com/BertrandBordage/django-cachalot), 因为发现这个最靠谱。

安装后发现，目前的版本只支持Django1.8, 而1.2.1版本不支持缓存时间设置，也就是CACHALOT_TIMEOUT设置，而线上服务器的Django正好是1.7版本，于是只好放弃。

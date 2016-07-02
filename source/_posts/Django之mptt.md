title: Django之mptt
date: 2016-07-02 21:30:22
tags:
    - Django
    - mptt
categories:
    - Python
---
在Web开发中，省/市/区(县)是经常需要用到的数据，而省/市/区(县)是一种层级关系。在使用Django做Web开发时，此时[Django-mptt](https://github.com/django-mptt/django-mptt)是一个很有用的模块。

首先执行`pip install django-mptt`安装django-mptt模块如[test-django](https://github.com/dengshilong/test-django)中示例那样，建立area应用，在area的models.py里添加如下model
```
#coding:utf-8
from __future__ import unicode_literals

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.

class Area(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', verbose_name=u'上级区域', null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        db_table = 'area'
        verbose_name = verbose_name_plural = (u'省/市/地区(县)')

    def __unicode__(self):
        return self.name
```

在area的admin.py里添加
```
from django.contrib import admin

# Register your models here.
from .models import Area


class AreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'level')
admin.site.register(Area, AreaAdmin)
```

在项目的settings里INSTALLED_APPS里添加mptt和area，之后执行数据库操作。之后在admin后台中就可以按照层级关系添加省/市/区(县)数据。

当然最好的方式还是用程序导入。从[统计局](http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2014/index.html)上爬取数据后导入到数据库中。

对于mptt要想深入理解的，可以参考这篇文章[hierarchical-data-database](https://www.sitepoint.com/hierarchical-data-database/)

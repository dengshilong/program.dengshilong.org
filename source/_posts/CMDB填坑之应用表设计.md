title: CMDB填坑之应用表设计
date: 2019-07-28 11:23:31
tags:
    - CMDB
categories:
---
CMDB填坑之应用表设计

自从负责CMDB后，很多问题都得自己亲自去面对，于是就得开始动动大脑，这时就发现之前设计不合理的地方。

如下是之前设计的应用表

```
class Application(Model):
    '''应用信息'''
    name = models.CharField(max_length=100, unique=True, help_text='应用名')
    language = models.CharField(max_length=64, help_text='应用语言')
```
    
这里数据是同步自另外一个系统，同步的时候只是把语言当做一个字段，这样也看不出什么问题。但是当应用数据源迁移自CMDB后，问题就来了。此时如果要创建一个应用，要有个应用语言列表供选择，然而CMDB里表设计的时候没有考虑语言表，所以没法提供相应的API。

综合考虑后，添加了语言表，并且在应用表下添加应用语言外键
    
```
class Language(Model):
    '''应用语言'''
    name = models.CharField(max_length=50, help_text='语言', unique=True)  
    
    
class Application(Model):
    '''应用信息'''
    name = models.CharField(max_length=100, unique=True, help_text='应用名')
    language = models.CharField(max_length=64, help_text='应用语言')
    language_fk = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True, db_constraint=False, help_text='语言')
```

最初的时候是考虑直接将应用表里的language改成外键，但想想这样修改会对之前提供出去的API有影响，所以还是决定添加language_fk外键。

这样修改后，需要创建应用时，写入language_fk的同时，也写入language即可，这个在Django里不难实现。

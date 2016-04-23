title: Django1.9.1使用django-pagination分页
date: 2016-04-23 18:16:20
tags: 
    - Django
categories:
    - Python
---
之前是用Django自带的[Paginator](https://docs.djangoproject.com/en/1.9/topics/pagination/)进行分页。在每一个需要分页的view都要添加分页处理，而使用django-pagination, 则只需要在模版里添加即可。于是开始使用django-pagination。使用的过程中发现以下问题

## 'WSGIRequest' object has no attribute 'REQUEST'

这是因为REQUEST对象已经在Django1.9中丢弃. 进入python的lib目录，进入lib/python2.7/site-packages／pagination, 将middleware.py里的return int(self.REQUEST['page'])改为return int(self.GET['page'])

## sequence index must be integer, not 'slice'
这是因为xrange对象不能进行slice操作，进入templatetags,将pagination_tags.py,paginate函数里的page_range = paginator.page_range改为 page_range = list(paginator.page_range)

很郁闷的是，django-pagination的github仓库里的程序没有更新，而且报TOKEN_BLOCK错误，估计是这个[commit](https://github.com/ericflo/django-pagination/commit/ef5ff95059866e94e89cad912c30497f90442765)中引入的。

于是只好fork出一份，自己修改。参见[product分支](https://github.com/dengshilong/django-pagination/tree/product)

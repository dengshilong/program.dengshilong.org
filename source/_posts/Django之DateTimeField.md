title: Django之DateTimeField
date: 2016-09-15 11:49:30
tags:
    - Django
    - DateTimeField
categories:
---
最近遇到一个[DateTimeField](https://docs.djangoproject.com/ja/1.10/ref/models/fields/#django.db.models.DateTimeField)的问题，记录下来

在Post的model里设置 
```
update_time = models.DateTimeField(auto_now=True)
```
希望每次更新文章时，这个update_time能自动更新为当前时间。

发现了三种情况
### 使用queryset的update方法
这里使用update方法更新，Post.object.filter(pk=id).update(), 发现不会更新update_time
### 使用save方法
```
post = Post.object.filter(pk=id)[:1][0]
post.save() 
```
此时会更新update_time
### 使用save方法，指定update_fields
```
post = Post.object.filter(pk=id)[:1][0]
post.save(update_fields=['title'])
```
此时指定了更新字段，不更新update_time

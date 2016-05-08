title: Django后台添加markdown编辑器
tags:
  - Django
  - markdown
id: 765
categories:
  - Python
date: 2014-06-22 16:42:36
---

在论坛和网上找了一下，发现django-pagedown可以满足需求，搜索之后，按照[https://pypi.python.org/pypi/django-pagedown/0.1.0](https://pypi.python.org/pypi/django-pagedown/0.1.0) 进行添加。

首先是安装
1. Get the code: `pip install django-pagedown`
2. Add `pagedown` to your `INSTALLED_APPS`
3. Make sure to collect the static files: `python manage.py collectstatic --noinput`

1.首先pip install django-pagedown下载

2.之后添加pagedown到项目的'INSTALLED_APPS'中，

3.执行命令python manage.py collectstatic --noinput，收集js,css等django-pagedown用到的静态文件。

之后开始添加，我的博客是在blog目录下,在目录里创建forms.py,添加如下内容

``` 
from pagedown.widgets import AdminPagedownWidget
from django import forms
from blog.models import Post

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=AdminPagedownWidget())
    class Meta:
        model = Post
```

这里是将content字段设置为markdown编辑，之后在admin.py中添加如下内容：
``` 
from django.contrib import admin
from blog.models import Post
from blog.forms import PostForm
class PostAdmin(admin.ModelAdmin):
    form = PostForm
admin.site.register(Post, PostAdmin)
```
搞定。这样之后，在编辑content时，在它的下方就会有一个markdown的解析成HTML的结果。这里，我在数据库中只保存了markdown的原始内容，显示时还需要将它解析成HTML，这个另外再说。

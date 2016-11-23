title: Django之context_processors
date: 2016-11-23 21:57:12
tags:
    - Django
    - context_processors
categories:
---
[context_processors](https://docs.djangoproject.com/en/1.10/ref/templates/api/#using-requestcontext)用于给Django模版添加context，例如[django.template.context_processors.media](https://docs.djangoproject.com/en/1.10/ref/templates/api/#django-template-context-processors-media)用于添加MEDIA_URL，[django.template.context_processors.static](https://docs.djangoproject.com/en/1.10/ref/templates/api/#django-template-context-processors-static)用于添加STATIC_URL。之所以使用context_processors, 是想全局添加某个变量，而不需要在每个View中添加。

查看django.template.context_processors.static的实现，就可以模仿着写自己的context_processors
```
def static(request):
    """
    Adds static-related context variables to the context.

    """
    return {'STATIC_URL': settings.STATIC_URL}
```

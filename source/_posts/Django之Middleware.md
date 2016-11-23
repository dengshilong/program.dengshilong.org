title: Django之Middleware
date: 2016-11-23 22:15:18
tags:
    - Django
    - Middleware
categories:
---
[Middleware](https://docs.djangoproject.com/en/1.10/topics/http/middleware/)相当于Django的底层插件，用于改变Django的输入和输出。最近遇到一个问题是有一些Android无法显示HTTPS页面中夹带的HTTP图片, 于是想到在返回结果中修改，于是想到Middleware.

编写一个Middleware也比较简单，根据需求定义响应的hook方法就好。这里定义如下
```
class StaticPathFilter(object):

    def process_response(self, request, response):
        if not response.streaming:
            if request.scheme == 'https':
                response.content = re.sub(r"http://static.eyaos.com", r"https://static.eyaos.com", response.content)
        return response
```
我这里是StaticPathFilter放在apps.common.middleware模块里, 把'apps.common.middleware.StaticPathFilter'添加到MIDDLEWARE_CLASSES即可。

title: Django跨域问题解决
date: 2018-07-12 19:16:17
tags:
    - Django
categories:
---
决定把自留地的前端代码独立开来，决定使用Vue来做。从0开始，遇到各种问题，打算记下来。最新遇到跨域问题，在访问服务的API时，报如下错误 No 'Access-Control-Allow-Origin' header is present on the requested resource，知道是跨域问题。看阮一峰[跨域资源共享 CORS 详解](http://www.ruanyifeng.com/blog/2016/04/cors.html)，知道跨域是怎么回事。

以前就知道Dango有[django-cors-headers](https://github.com/ottoyiu/django-cors-headers)模块用来支持跨域, 只是没有自己配置过。按照文档进行配置，加上白名单

```
CORS_ORIGIN_WHITELIST = (
    '127.0.0.1:8081',
)
```

发现还是报相同的错误，改成

```
CORS_ORIGIN_WHITELIST = (
    '127.0.0.1:8081',
    'localhost:8081',
)
```

后就没有这个问题了。说明localhost和127.0.0.1是有区别的。

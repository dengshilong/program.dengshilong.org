title: CSRF匹配失败错误查找
date: 2018-08-02 19:26:47
tags:
    - Django
categories:
---
同事发了下面一个错误, 让我复现并找到解决的办法。错误原因是www.example.com的前端页面访问后端api.example.com出错。

```
{
    "detail":"CSRF Failed: Referer checking failed - 
    https://www.example.com/ does not match any trusted origins."
    
}
```

在[CSRF validation does not work on Django using HTTPS](https://stackoverflow.com/questions/38841109/csrf-validation-does-not-work-on-django-using-https/38842030)中找到类似的错误，但是不知道怎么复现，在[Issue with CsrfViewMiddleware and "referer" same_origin checking for secure (https) subdomains](https://github.com/encode/django-rest-framework/issues/2982)中发现有可能是CsrfViewMiddleware检测的原因。

于是才想起来可以用将"does not match any trusted origins"放到Django源码中搜索下，果然是在CsrfViewMiddleware里，于是将一些代码注释掉，知道在settings里配置一下CSRF_TRUSTED_ORIGINS即可，于是添加CSRF_TRUSTED_ORIGINS = ['example.com'], 问题解决。

整个解决过程现在回想起来有些浪费时间，最有效的方法还是拿关键字到源码中找到对应代码，看看报错原因。

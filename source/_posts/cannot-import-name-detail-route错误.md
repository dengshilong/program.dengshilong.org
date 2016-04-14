title: cannot import name detail_route错误
date: 2016-04-14 20:17:02
tags: 
    - Django
categories: 
    - Python
---
在看[Django-rest-framework2](http://tomchristie.github.io/rest-framework-2-docs/)时，看到Tutorial 6: ViewSets & Routers，执行`from rest_framework.decorators import detail_route`时，报cannot import name detail_route错误

查看decorators.py源码，发现原因是从2.4.0才有这个方法，而公司用的是2.3.14，所以没有。

在view里添加detail_route的代码
```
def detail_route(methods=['get'], **kwargs):
    """ 
    Used to mark a method on a ViewSet that should be routed for detail requests.
    """
    def decorator(func):
        func.bind_to_methods = methods
        func.detail = True
        func.kwargs = kwargs
        return func
    return decorator
```


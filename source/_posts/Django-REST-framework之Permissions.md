title: Django-REST-framework之Permissions
date: 2016-08-07 14:54:40
tags:
    - Django
    - REST
categories:
    - Python
---
在使用Django REST framework时，对接口加上权限限制是必不可少的，例如对于一篇文章，只有管理员和作者才有删除的权限，其它人只能有读取权限。此时[Permissions](
http://www.django-rest-framework.org/api-guide/permissions/)就派上用场了。

REST framework提供了很多种权限，如IsAuthenticated，IsAdminUser等等，要定制permissions, 也是很容易的一件事。要定制permissions, 只需继承BasePermission，然后实现其中一个或者两个方法
* has_permission(self, request, view)
* has_object_permission(self, request, view, obj)

其中，has_permission是相对接口而言的，也就是在访问这个接口时，会进行权限检测。而has_object_permission是相对于对象而言的，只有访问对象时才会进行权限检测。

还有一个问题是，当实现自己的get_object并且需要进行权限检查时，不要忘记调用`self.check_object_permissions(self.request, obj)`
```
def get_object(self):
    obj = get_object_or_404(self.get_queryset())
    self.check_object_permissions(self.request, obj)
    return obj
```

而对于访问对象进行权限检测时，一个好的方法是如果是安全方法如GET, HEAD等，则运行访问。
```
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.owner == request.user
```

title: Django之REST
date: 2016-07-03 11:37:27
tags:
    - Django
    - REST
categories:
    - Python
---
在Django开发过程中，要实现REST api时，[Django REST framework](http://www.django-rest-framework.org/)是一个很不错的模块。

拿前面的[省/市/区(县)](http://program.dengshilong.org/2016/07/03/Django%E4%B9%8Bcache/)的例子来说，假设我们要提供一个返回某个省份下所有城市的api。

* 安装Django REST framework，
执行`pip install djangorestframework`进行安装, 在项目的settings的INSTALLED_APPS里添加'rest_framework'
* 在area应用里添加api.py文件，内容如下, API View如何编写参看[generic-views](http://www.django-rest-framework.org/api-guide/generic-views/)
```
from rest_framework import generics
from .cache import city_cache
from .serializer import AreaSerializer
class CityListAPI(generics.ListAPIView):
    serializer_class = AreaSerializer

    def get_queryset(self):
        return city_cache(self._province)

    def get(self, request, *args, **kwargs):
        self._province = kwargs['province']
        return super(CityListAPI, self).get(request, *args, **kwargs)
```
在代码里我们看到city_cache的调用，这里就是用的之前介绍的cache
* 在area应用里添加serizlizer.py文件，添加序列化, 序列化如何编写参看[serializers](http://www.django-rest-framework.org/api-guide/serializers/)
```
from rest_framework import serializers
from .models import Area


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ('id', 'name', 'level')
```
* 在area中添加urls.py文件，内容如下
```

from django.conf.urls import patterns, url

from .api import CityListAPI

urlpatterns = patterns('',
    url(r'^api/city/list/(?P<province>\d+)$', CityListAPI.as_view(), name='city_list'),
)
```
* 在项目的urls.py里添加area的url
 `url(r'area/', include('area.urls'))`

之后启动服务，就可以访问http://127.0.0.1:8000/area/api/city/list/1 看到结果。

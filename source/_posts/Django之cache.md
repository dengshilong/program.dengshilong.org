title: Django之cache
date: 2016-07-03 10:55:30
tags:
    - Django
    - cache
categories:
    - Python
---
在前面的省/市/区(县)的例子中，如果查询某个省下面的市信息是一个常用的操作时，此时可以使用缓存。

Django提供了[cache](https://docs.djangoproject.com/ja/1.9/topics/cache/)功能，只需要进行简单配置就可以使用。缓存可以保存在很多地方，如Memcached, Redis等，这里以Redis为例。

按照[django-redis](https://github.com/niwinz/django-redis)的[官方文档](http://niwinz.github.io/django-redis/latest/), `pip install django-redis`进行安装。在项目的settings.py里添加如下配置
```
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
```
之后就可以使用缓存了。在area应用里添加cache.py文件，添加如下内容
```
#coding:utf-8
from django.core.cache import cache
from .models import Area

def city_cache(province):
    """市"""
    key = 'city_list_%s' % province
    cities = cache.get(key)
    if cities is None:
        cities = list(Area.objects.filter(parent_id=province))
        cache.set(key, cities, 36000)
    return cities
```
这样调用city_cache时，传入省份id，就可以得到这个省下面的所有市的列表。

具体操作可以参看我在github上的[test-django](https://github.com/dengshilong/test-django)仓库

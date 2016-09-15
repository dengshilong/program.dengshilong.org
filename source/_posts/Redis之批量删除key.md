title: Redis之批量删除key
date: 2016-09-15 10:05:57
tags:
    - Redis
    - del
categories:
---
Redis提供了[del](http://redis.io/commands/del)命令来删除key, 但并没有提供批量删除key的命令，此时可以使用Linux的xargs命令来辅助完成。

例如在使用[django-cachalot)(https://github.com/BertrandBordage/django-cachalot)来给Django的queryset做缓存时，想要删除以":1:"开头的key, 就可以使用如下命令
`redis-cli -n 0 keys ":1:*" | xargs redis-cli -n 0 del`  

title: Django之Signals
date: 2016-07-03 14:49:01
tags:
    - Django
    - Signals
categories:
    - Python
---
在[Django之cache](http://program.dengshilong.org/2016/07/03/Django%E4%B9%8Bcache/)的例子中，我们使用了缓存。但这里存在一个问题，当我们添加了数据后，因为缓存是有实效的，里面的数据没有更新。此时需要有一个机制，当我们更新的model的数据时，要清除缓存。Django提供的[Signals](
https://docs.djangoproject.com/es/1.9/ref/signals/)可以满足这个需求。

在model保存和删除时，需要进行清除缓存。这里用到post_save和post_delete两个信号。

在area的models.py里添加如下代码
```
@receiver(post_delete, sender=Area)
@receiver(post_save, sender=Area)
def delete_cache(sender, **kwargs):
    #清除cache
    obj = kwargs['instance']
    if obj.parent is None:
        key = "city_list_0"
    else:
        key = "city_list_%s" % obj.parent_id
    cache.delete(key)
```

之后在admin后台添加和删除数据时，缓存就会被清除。访问http://127.0.0.1:8000/area/api/city/list/1 时就可以读取到最新的数据 

想自己尝试的可以下载[test-django](https://github.com/dengshilong/test-django)

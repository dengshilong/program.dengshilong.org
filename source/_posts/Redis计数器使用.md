title: Redis计数器使用
date: 2016-10-22 15:20:43
tags:
    - Redis
    - 计数器
categories:
---
最近从公司APP分享出去的一篇文章，访问量暴增，而访问计数直接访问的数据库，数据库产生行级锁，许多访问超时。
```
News.objects.filter(pk=self.object.id).update(view_num=F('view_num') + 1)
```
临时把访问计数去掉。之后找到Redis计数器。在访问文章时，使用incr自增。只是在访问文章列表时，如果对每篇文章都要读一次Redis会影响性能，于是只好做了延时处理，每个一段时间同步到数据库，并进行清零，等想到更好的解决办法再说。

清零时，最好不要使用`set key 0`这种用法，在多线程情况下会出问题，目前使用`incrby key -view_num`这种方式, 也就是减去目前Redis中浏览量的方式。

Redis确实是好东西，需要深入学习。

参考资料
* [Redis之INCR命令](http://redisdoc.com/string/incr.html)
* [Redis 使用模式之一：计数器](http://xiewenwei.github.io/blog/2014/07/06/redis-use-pattern-1-counter/)

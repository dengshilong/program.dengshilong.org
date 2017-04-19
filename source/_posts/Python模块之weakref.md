title: Python模块之weakref
date: 2017-04-19 14:08:13
tags:
    - Python
    - weakref
categories:
---
看blinker源码时，看到[weakref](https://docs.python.org/3/library/weakref.html)，也就是弱引用模块，以前看《Fluent Python》时也有看到过，只是没有再实际场景中用过。看介绍，主要是用在缓存时对象释放，以及循环引用等场景。[PEP-205](http://www.python.org/dev/peps/pep-0205/)有结束这个模块的由来。

下面是一个缓存使用中的例子，先声明一个Cheese类
```
class Cheese(object):

    def __init__(self, kind):
        self.kind = kind

    def __repr__(self):
        return 'Cheese(%r)' % self.kind
```
之后在交互环境中执行如下操作

```
>>> import weakref
>>> stock = weakref.WeakValueDictionary()
>>> catalog = [Cheese('Red Leicester'), Cheese('Tilsit'), Cheese('Brie'), Cheese('Parmesan')]
>>> for cheese in catalog:
...     stock[cheese.kind] = cheese
...
>>> sorted(stock.keys())
['Brie', 'Parmesan', 'Red Leicester', 'Tilsit']
>>> del catalog
>>> sorted(stock.keys())
['Parmesan']
>>> del cheese
>>> sorted(stock.keys())
[]
```
可以看到当删除catelog对象时，在stock中的对象会自动释放。

对于循环引用的例子，可以参考[Python 弱引用的使用](http://www.jianshu.com/p/0cecea85ae3b)

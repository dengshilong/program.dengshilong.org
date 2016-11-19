title: Python之Descriptor描述器
date: 2016-11-19 21:04:52
tags:
    - Python
    - Descriptor
    - 描述器
categories:
---
最近在看Django文档[Making queries](https://docs.djangoproject.com/en/1.9/topics/db/queries/)时看到[descriptor](http://users.rcn.com/python/download/Descriptor.htm), 发现描述器很强大.

> Descriptors are a powerful, general purpose protocol. They are the mechanism behind properties, methods, static methods, class methods, and super(). They are used used throughout Python itself to implement the new style classes introduced in version 2.2. Descriptors simplify the underlying C-code and offer a flexible set of new tools for everyday Python programs.

但是我还是不懂为什么需要描述符，直到看了[Python描述符(descriptor)解密](http://pyvideo.org/pycon-us-2013/encapsulation-with-descriptors.html), 才知道描述符的用途。按照视频中的讲解，在理解一遍，加深印象。

假设在做一个农产品销售系统，每个订单是一个产品，每个产品有description, weight, price三个字段

```
class LineItem(object):

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price
```
但这里存在一个问题，即weight可以为负的。
```
>>> raisins = LineItem('Golden raisins', 10, 6.95)
>>> raisins.subtotal()
69.5
>>> raisins.weight = -20 #负值
>>> raisins.subtotal()
-139.0
```

这是一个严重的问题，亚马逊刚起步时就有这个问题。 在[Jeff Bezos and Amazon: Birth of a Salesman](http://www.wsj.com/articles/SB10001424052970203914304576627102996831200)里有描述。

传统的做法是添加getter和setter方法
```
class LineItem(object):

    def __init__(self, description, weight, price):
        self.description = description
        self.set_weight(weight)
        self.price = price

    def subtotal(self):
        return self.get_weight() * self.price

    def get_weight(self):
        return self.__weight

    def set_weight(self, value):
        if value > 0:
            self.__weight = value
        else:
            raise ValueError('value must be > 0')


if __name__ == "__main__":
    raisins = LineItem('Golden raisins', 10, 6.95)
    print raisins.subtotal()
    raisins.weight
    print raisins.subtotal()
```

这种方法存在一些问题，
* 之前可以使用raisins.weight, 现在不能使用
* 和以前的代码不兼容，以前可以使用raisins.weight, 现在必须raisins.get_weight和set_weight

好在Python提供更好的解决办法, property是其中一种
```
class LineItem(object):

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, value):
        if value > 0:
            self.__weight = value
        else:
            raise ValueError('value must be > 0')


if __name__ == "__main__":
    raisins = LineItem('Golden raisins', 10, 6.95)
    print raisins.subtotal()
    print raisins.weight
    print raisins.subtotal()
    raisins.weight = -2.0
```
使用property存在一个问题是，当我们需要对price也做非0限制时，需要重复setter设置。此时Descriptor派上用场了。
```
class Quantity(object):
    __counter = 0
    def __init__(self):
        prefix = '_' + self.__class__.__name__
        key = self.__class__.__counter
        self.target_name = '%s_%s' % (prefix, key)
        self.__class__.__counter += 1

    def __get__(self, instance, owner):
        return getattr(instance, self.target_name)

    def __set__(self, instance, value):
        if value > 0:
            setattr(instance, self.target_name, value)
        else:
            raise ValueError('value must be > 0')

class LineItem(object):
    weight = Quantity()
    price = Quantity()

    def __init__(self, description, weight, price):
        self.description = description
        self.weight = weight
        self.price = price
    
    def subtotal(self):
        return self.weight * self.price


if __name__ == "__main__":
    raisins = LineItem('Golden raisins', 10, 6.95)
    print raisins.subtotal()
    print raisins.weight
    print raisins.subtotal()
    raisins.weight = -2.0
    raisins.price = -1
```
在Quantity类里, instance是指LineItem实例, owner指LineItem类。

具体查看视频，非常不错。


参考资料
* [Descriptor HowTo Guide(https://docs.python.org/3/howto/descriptor.html)
* [Unifying types and classes in Python 2.2](https://www.python.org/download/releases/2.2.3/descrintro/)

title: Python程序设计入门之metaprogramming
date: 2019-09-06 21:46:11
tags:
    - Python
categories:
---
前些天在看David Beazley的[Python3 metaprogramming](https://www.youtube.com/watch?v=sPiWg5jSoZI)视频，觉得是时候总结下视频中学到的内容, 这篇文章主要是这个视频的笔记，以及关于metaclass的一些思考.

## 装饰器
首先看一个需求，就是想在函数被调用时，记录一下，可以简单的加个print

```
def add(x, y):
    print('add')
    return x + y

def sub(x, y):
    print('sub')
    return x - y

def mul(x, y):
    print('mul')
    return x * y

def div(x, y):
    print('div')
    return x / y

print(add(3, 5))
print(sub(5, 2))

输出
add
8
sub
3
```

但是这样的话, print语句就重复了, 每个函数里都得加print, 于是我们可以使用装饰器

```
# 一个简单的装饰器
def debug(func):
    def wrapper(*args, **kwargs):
        print(func.__name__)
        return func(*args, **kwargs)
    return wrapper

@debug
def add(x, y):
    return x + y

@debug
def sub(x, y):
    return x - y

@debug
def mul(x, y):
    return x * y

@debug
def div(x, y):
    return x / y

print(add(3, 5))
print(sub(5, 2))

输出
add
8
sub
3
```
### 使用functools
但是这个简单的装饰器是存在问题的，它会忽略被装饰的函数

```
print(add)

输出
<function debug.<locals>.wrapper at 0x1037a6bf8>
```
这里add函数经过debug装饰器装饰后，函数名都被忽略了，这个时候functools模块就派上用场了, 里面的wraps装饰器就是用来解决这个问题

```
from functools import wraps

def debug(func):
    msg = func.__qualname__
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(msg)
        return func(*args, **kwargs)
    return wrapper
    
@debug
def add(x, y):
    return x + y

@debug
def sub(x, y):
    return x - y

@debug
def mul(x, y):
    return x * y

@debug
def div(x, y):
    return x / y

print(add(3, 5))
print(sub(5, 2))

输出
add
8
sub
3

print(add)
输出
<function add at 0x1037afa60>
```
### 带参数的装饰器
有时候装饰器里想传入一些参数, 这时就可以写带参数的装饰器
```
# decorators with args
from functools import wraps

def debug(prefix=''):
    def decroate(func):
        msg = prefix + func.__qualname__
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(msg)
            return func(*args, **kwargs)
        return wrapper
    return decroate

@debug('###')
def add(x, y):
    return x + y

print(add(3, 2))
输出
###add
5
```
这种带参数的装饰器有一个头疼的问题是, 使用装饰器时, 如果不想传参数, 也得加上括号, 不然会报错

```
@debug
def sub(x, y):
    return x - y

sub(5, 3)

---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
<ipython-input-40-9a93be17056c> in <module>
      3     return x - y
      4 
----> 5 sub(5, 3)

TypeError: decroate() takes 1 positional argument but 2 were given
```
加上括号后, 就不报错, 这很丑陋
```
@debug()
def sub(x, y):
    return x - y

print(sub(5, 3))
```
这里有一个小技巧, 实现如下
```
from functools import wraps, partial

def debug(func=None, prefix=''):
    if func is None:
        return partial(debug, prefix=prefix)
    msg = prefix + func.__qualname__
    @wraps(func)
    def wrapper(*args, **kwargs):     
        print(msg)
        return func(*args, **kwargs)
    return wrapper
```
如此, 当使用默认参数时, 即便不带括号时，也不会报错
```
@debug(prefix='###')
def add(x, y):
    return x + y


@debug
def sub(x, y):
    return x - y

print(add(3, 2))
print(sub(5, 3))
输出
###add
5
sub
2
```
### 类装饰器
以下我们定义一个Spam类,
```
class Spam:
    def a(self):
        pass
    def b(self):
        pass
    @classmethod
    def c(cls):
        pass
    @staticmethod
    def d():
        pass
```
然后我们想在类的方法被调用时, 能够记录下, 想上面的函数被调用时一样, 这时我们就会可以编写一个类装饰器
```
def debugmethods(cls):
    # cls is class
    for key, val in vars(cls).items():
        if callable(val):
            setattr(cls, key, debug(val))
    return cls

@debugmethods
class Spam:
    def a(self):
        pass
    def b(self):
        pass
    @classmethod
    def c(cls):
        pass
    @staticmethod
    def d():
        pass

spam = Spam()
spam.a()
spam.b()
spam.c()
spam.d()
输出
Spam.a
Spam.b
```
这里只打印了a和b, 没有打印c和d, 这什么原因呢? 这是因为classmethod和staticmethod都是descriptor, 也就是描述器, 它们没有实现`__call__`方法，也就不是callable的

我们也可以编写一个类装饰器, 当获取一个属性时, 打印日志
```
# debug access
def debugattr(cls):
    orig_getattribute = cls.__getattribute__
    def __getattribute__(self, name):
        print('Get:', name)
        return orig_getattribute(self, name)
    cls.__getattribute__ = __getattribute__
    return cls

@debugattr
class Spam:
    def __init__(self, x, y):
        self.x = x
        self.y = y

spam = Spam(2, 3)
print(spam.x)
输出
Get: x
2
```
## metaclass
现在我们想对所有的类都能打印日志，一个解决的办法是在所有的类前面都加上类装饰器
```
@debugmethods
class Base:
    def a(self):
        pass
    def b(self):
        pass
    
@debugmethods
class Spam(Base):
    def a(self):
        pass
b = Base()
b.a()
s = Spam()
s.a()
输出
Base.a
Spam.a
```
但这样很麻烦，于是metaclass派上用场了, metaclass最强的地方是可以控制类的创建

```
# a metaclass
class debugmeta(type):
    def __new__(cls, clsname, bases, clsdict):
        clsobj = super().__new__(cls, clsname, bases, clsdict)
#         print("here", cls, clsname, type(clsobj), clsobj)
        clsobj = debugmethods(clsobj)
#         print(vars(clsobj))
        return clsobj

class Base(metaclass=debugmeta):
    def a(self):
        pass
    def b(self):
        pass

    
class Spam(Base):
    def __init__(self, name):
        self.name = name
        
    def a(self):
        pass
    
b = Base()
b.a()
s = Spam('name')
s.a()

输出
Base.a
Spam.__init__
Spam.a
```
从上面的例子中我们看到，有一个类有metaclass, 它的所有子类都有metaclass, 这说明metaclass是会被继承的。结合蔡元楠的《metaclass, 是潘多拉魔盒还是阿拉丁神灯》, 可以知道，这里debugmeta其实不只一种写法，在`__init__`函数里实现也是可以的。重载`__init__`的实现如下
```
# a metaclass
class debugmeta(type):
     def __init__(cls, name, bases, kwds):
        super(debugmeta, cls).__init__(name, bases, kwds)
        cls = debugmethods(cls)

class Base(metaclass=debugmeta):
    def a(self):
        pass
    def b(self):
        pass

    
class Spam(Base):
    def __init__(self, name):
        self.name = name
        
    def a(self):
        pass
b = Base()
b.a()
s = Spam('lala')
s.a()
输出
Base.a
Spam.__init__
Spam.a
```
这是因为, 所有的类都是type的实例, 都是对type的`__call__`方法进行重载, 而type的`__call__`方法会调用`type.__new__(typeclass, classname, superclasses, attributedict)`和`type.__init__(class, classname, superclasses, attributedict)`, 所以上面重写`__new__`和重写`__init__`都是可以的。

学到这里，我脑海里冒出了一个想法，就是为啥这里一定要用metaclass呢? 用继承的方式难道不行吗？于是自己尝试写了个继承的方式, 发现也是跑得通的。

```
# a baseclass
class debugmeta:
    def __new__(cls, *args, **kwargs):
        cls = debugmethods(cls)
        clsobj = object.__new__(cls)
#         clsobj = debugmethods(clsobj)
#         print('aaa', type(clsobj), clsobj)
#         print('aaa', clsobj, type(clsobj), vars(clsobj), dir(clsobj), type(clsobj.a), callable(clsobj.a))
        return clsobj
    
class Base(debugmeta):
    def a(self):
        pass

    
class Spam(Base):
    def __init__(self, name):
        self.name = name
    def a(self):
        pass

    
b = Base()
b.a()
s = Spam('name')
s.a()
输出
Base.a
Spam.__init__
Spam.a
```
既然如此，那么蔡元楠在《metaclass, 是潘多拉魔盒还是阿拉丁神灯》介绍的yaml的动态序列化和逆序列化的能力又为何要用metaclass实现呢？用继承难道不行吗？于是也写了一个继承的版本, 代码如下。
```
import yaml


class MyYAMLObjectBaseclass(object):
    """
    The metaclass for YAMLObject.
    """
    def __new__(cls, *args, **kwargs):
        if cls.yaml_tag:
            cls.yaml_loader.add_constructor(cls.yaml_tag, cls.from_yaml)
            cls.yaml_dumper.add_representer(cls, cls.to_yaml)
        return object.__new__(cls)

class MyYAMLObject(MyYAMLObjectBaseclass):
    """
    An object that can dump itself to a YAML stream
    and load itself from a YAML stream.
    """

    __slots__ = ()  # no direct instantiation, so allow immutable subclasses

    yaml_loader = yaml.Loader
    yaml_dumper = yaml.Dumper

    yaml_tag = None
    yaml_flow_style = None

    @classmethod
    def from_yaml(cls, loader, node):
        """
        Convert a representation node to a Python object.
        """
        return loader.construct_yaml_object(node, cls)

    @classmethod
    def to_yaml(cls, dumper, data):
        """
        Convert a Python object to a representation node.
        """
        return dumper.represent_yaml_object(cls.yaml_tag, data, cls,
                flow_style=cls.yaml_flow_style)


class Monster(MyYAMLObject):
    yaml_tag = '!Monster'

    def __init__(self, name, hp, ac, attacks):
        self.name = name
        self.hp = hp
        self.ac = ac
        self.attacks = attacks

    def __repr__(self):
        return "{}(name={}, hp={}, ac={}, attacks={}".format(self.__class__.__name__, self.name, self.hp,
                                                             self.ac, self.attacks)


class Dragon(Monster):
    yaml_tag = '!Dragon'

    def __init__(self, name, hp, ac, attacks, energy):
        super(Dragon, self).__init__(name, hp, ac, attacks)
        self.energy = energy

    def __repr__(self):
        return "{}(name={}, hp={}, ac={}, attacks={}, energy={})".format(self.__class__.__name__, self.name, self.hp,
                                                             self.ac, self.attacks, self.energy)

m = Monster(name='Cave spider', hp=[2, 6], ac=16, attacks=['BITE', 'HURT'])
ms = yaml.dump(m)
# print(ms)
d = Dragon(name='Cave spider', hp=[2, 6], ac=17, attacks=['BITE', 'HURT'], energy=5000)
ds = yaml.dump(d)
# print(ds)

print(yaml.load(ms, Loader=yaml.Loader))
print(yaml.load(ds, Loader=yaml.Loader))
输出
Monster(name=Cave spider, hp=[2, 6], ac=16, attacks=['BITE', 'HURT']
Dragon(name=Cave spider, hp=[2, 6], ac=17, attacks=['BITE', 'HURT'], energy=5000)
```
所以其实到这里我还是没有明白为啥yaml要用metaclass来实现这个功能, 直到把子类的yaml_tag去掉, 才发现问题。
```
import yaml


class Monster(MyYAMLObject):
    yaml_tag = '!Monster'

    def __init__(self, name, hp, ac, attacks):
        self.name = name
        self.hp = hp
        self.ac = ac
        self.attacks = attacks

    def __repr__(self):
        return "{}(name={}, hp={}, ac={}, attacks={}".format(self.__class__.__name__, self.name, self.hp,
                                                             self.ac, self.attacks)


class Dragon(Monster):

    def __init__(self, name, hp, ac, attacks, energy):
        super(Dragon, self).__init__(name, hp, ac, attacks)
        self.energy = energy

    def __repr__(self):
        return "{}(name={}, hp={}, ac={}, attacks={}, energy={})".format(self.__class__.__name__, self.name, self.hp,
                                                             self.ac, self.attacks, self.energy)

m = Monster(name='Cave spider', hp=[2, 6], ac=16, attacks=['BITE', 'HURT'])
ms = yaml.dump(m)
# print(ms)
d = Dragon(name='Cave spider', hp=[2, 6], ac=17, attacks=['BITE', 'HURT'], energy=5000)
ds = yaml.dump(d)
# print(ds)

print(yaml.load(ms, Loader=yaml.Loader))
print(yaml.load(ds, Loader=yaml.Loader))
输出
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
<ipython-input-58-1e3c4c44fbaf> in <module>
     33 # print(ds)
     34 
---> 35 print(yaml.load(ms, Loader=yaml.Loader))
     36 print(yaml.load(ds, Loader=yaml.Loader))

<ipython-input-58-1e3c4c44fbaf> in __repr__(self)
     24     def __repr__(self):
     25         return "{}(name={}, hp={}, ac={}, attacks={}, energy={})".format(self.__class__.__name__, self.name, self.hp,
---> 26                                                              self.ac, self.attacks, self.energy)
     27 
     28 m = Monster(name='Cave spider', hp=[2, 6], ac=16, attacks=['BITE', 'HURT'])

AttributeError: 'Dragon' object has no attribute 'energy'
```
这是因为Dragon这里没有yaml_tag的时候, 会继承父类Monster的yaml_tag, 这时Dragon.yaml_tag就是非空, 然后就会将!Monster这个标记与Dragon绑定到一起了, 覆盖了前面!Monster与Monster的绑定, 这时再去加载Monster类dump出来的内容, 就会报没有energy. 而使用metaclass就不存在这个问题, 因为在创建Dragon类时, 传入的属性字典里不会带有yaml_tag, 也就不会将!Monster这个标记与Dragon绑定到一起. 写代码测试如下
```
import yaml


class MyYAMLObjectMetaclass(type):
    """
    The metaclass for YAMLObject.
    """
    def __new__(cls, name, bases, kwds):
        print(cls, name, bases, kwds.get('yaml_tag', 'hahaha'))
        clsobj = super().__new__(cls, name, bases, kwds)
        if 'yaml_tag' in kwds and kwds['yaml_tag'] is not None:
            clsobj.yaml_loader.add_constructor(clsobj.yaml_tag, clsobj.from_yaml)
            clsobj.yaml_dumper.add_representer(clsobj, clsobj.to_yaml)
        return clsobj

class ThisYAMLObjectMetaclass(type):
    """
    The metaclass for YAMLObject.
    """
    def __init__(cls, name, bases, kwds):
        print(cls, name, bases, kwds.get('yaml_tag', 'hahaha'))
        super(ThisYAMLObjectMetaclass, cls).__init__(name, bases, kwds)
        if 'yaml_tag' in kwds and kwds['yaml_tag'] is not None:
            cls.yaml_loader.add_constructor(cls.yaml_tag, cls.from_yaml)
            cls.yaml_dumper.add_representer(cls, cls.to_yaml)


class ThisYAMLObjectBaseclass(object):
    """
    The metaclass for YAMLObject.
    """
    def __new__(cls, *args, **kwargs):
        print('base __new__', cls, args, kwargs)
        if cls.yaml_tag:
            cls.yaml_loader.add_constructor(cls.yaml_tag, cls.from_yaml)
            cls.yaml_dumper.add_representer(cls, cls.to_yaml)
        return object.__new__(cls)


class MyYAMLObject(metaclass=ThisYAMLObjectMetaclass):
# class MyYAMLObject(ThisYAMLObjectBaseclass):
# class MyYAMLObject(metaclass=MyYAMLObjectMetaclass):
    """
    An object that can dump itself to a YAML stream
    and load itself from a YAML stream.
    """

    __slots__ = ()  # no direct instantiation, so allow immutable subclasses

    yaml_loader = yaml.Loader
    yaml_dumper = yaml.Dumper

    yaml_tag = None
    yaml_flow_style = None

    @classmethod
    def from_yaml(cls, loader, node):
        """
        Convert a representation node to a Python object.
        """
        return loader.construct_yaml_object(node, cls)

    @classmethod
    def to_yaml(cls, dumper, data):
        """
        Convert a Python object to a representation node.
        """
        return dumper.represent_yaml_object(cls.yaml_tag, data, cls,
                flow_style=cls.yaml_flow_style)


class Monster(MyYAMLObject):
    yaml_tag = '!Monster'

    def __init__(self, name, hp, ac, attacks):
        self.name = name
        self.hp = hp
        self.ac = ac
        self.attacks = attacks

    def __repr__(self):
        return "{}(name={}, hp={}, ac={}, attacks={}".format(self.__class__.__name__, self.name, self.hp,
                                                             self.ac, self.attacks)


class Dragon(Monster):
    # yaml_tag = '!Dragon'

    def __init__(self, name, hp, ac, attacks, energy):
        super(Dragon, self).__init__(name, hp, ac, attacks)
        self.energy = energy

    def __repr__(self):
        return "{}(name={}, hp={}, ac={}, attacks={}, energy={})".format(self.__class__.__name__, self.name, self.hp,
                                                             self.ac, self.attacks, self.energy)

m = Monster(name='Cave spider', hp=[2, 6], ac=16, attacks=['BITE', 'HURT'])
ms = yaml.dump(m)
# print(ms)
d = Dragon(name='Cave spider', hp=[2, 6], ac=17, attacks=['BITE', 'HURT'], energy=5000)
ds = yaml.dump(d)
# print(ds)

print(yaml.load(ms, Loader=yaml.Loader))
print(yaml.load(ds, Loader=yaml.Loader))
输出
<class '__main__.MyYAMLObject'> MyYAMLObject () {'__module__': '__main__', '__qualname__': 'MyYAMLObject', '__doc__': '\n    An object that can dump itself to a YAML stream\n    and load itself from a YAML stream.\n    ', '__slots__': (), 'yaml_loader': <class 'yaml.loader.Loader'>, 'yaml_dumper': <class 'yaml.dumper.Dumper'>, 'yaml_tag': None, 'yaml_flow_style': None, 'from_yaml': <classmethod object at 0x1038e9320>, 'to_yaml': <classmethod object at 0x1038e9390>}
<class '__main__.Monster'> Monster (<class '__main__.MyYAMLObject'>,) {'__module__': '__main__', '__qualname__': 'Monster', 'yaml_tag': '!Monster', '__init__': <function Monster.__init__ at 0x1038d2f28>, '__repr__': <function Monster.__repr__ at 0x1038ce048>}
<class '__main__.Dragon'> Dragon (<class '__main__.Monster'>,) {'__module__': '__main__', '__qualname__': 'Dragon', '__init__': <function Dragon.__init__ at 0x1038ce0d0>, '__repr__': <function Dragon.__repr__ at 0x1038ce158>, '__classcell__': <cell at 0x103837af8: ThisYAMLObjectMetaclass object at 0x7fc8fb130de8>}
Monster(name=Cave spider, hp=[2, 6], ac=16, attacks=['BITE', 'HURT']
Dragon(name=Cave spider, hp=[2, 6], ac=17, attacks=['BITE', 'HURT'], energy=5000)
```
从上面的结果里可以看到, yaml_tag是没有在Dragon类的属性字典里的，即便是Dragon类会从Monster那里继承yaml_tag.

到了这里, 我终于明白为什么yaml要使用metaclass, 而不是继承了。

总的来说, metaclass并不是什么奇淫巧技，简单来说就是一种改变类创建过程的能力。当然, 绝大多数情况下都不需要用到它。

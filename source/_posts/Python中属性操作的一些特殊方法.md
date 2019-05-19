title: Python中属性操作的一些特殊方法
date: 2017-06-04 21:22:43
tags:
    - Python
categories:
---
Python中内置的一些属性相关的函数，如dir, getattr, hasattr, setattr, vars, 这里主要来看看一些特殊方法

编写测试代码如下：

```
class Class:
    def __delattr__(self, name):
        print('## delattr')
        super().__delattr__(name)

    def __getattr__(self, name):
        print('## getattr')
        return 'default'

    def __getattribute__(self, name):
        print('## getattribute')
        super().__getattribute__(name)

    def __setattr__(self, name, value):
        print('## setattr')
        super().__setattr__(name, value)


if __name__ == "__main__":
    c = Class()
    getattr(c, 'name')
    print("-----")
    c.name
    print("-----")
    c.data = 'test'
    print("-----")
    c.data
    print("-----")
    del c.data
```

得到输出结果

```
## getattribute
## getattr
-----
## getattribute
## getattr
-----
## setattr
-----
## getattribute
-----
## delattr
```

可以看到c.name和getattr(c, 'name')都会调用`__getattribute__`方法，之后调用`__getattr__`方法，c.data = 'test'会调用`__setattr__`方法，之后c.data只调用了`__getattribute__`方法, del c.data调用了`__delattr__`方法。

所以可以总结如下
* `__getattribute__`在获取属性时都会被调用到
* `__getattr__`当对象没有相应的属性时，会被调用
* `__setattr__`在设置属性时会被调用
* `__delattr__`在删除属性时会被调用

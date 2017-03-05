title: Python闭包与nonlocal
date: 2017-03-03 10:53:30
tags:
    - Python
    - 闭包
    - nonlocal
categories:
---
《Fluent Python》里说，简单来说，闭包就是一个包含非全局变量且该变量不是在它自己函数体里声明的函数。它不关系函数是否匿名，它关心的是可以访问不在自己函数体里定义的非全局变量。

考虑一个avg平均值函数，如下

```
>>> avg(10) 
10.0
>>> avg(11) 
10.5
>>> avg(12) 
11.0
```
一个使用类的方法如下
```
class Averager():
    """
    >>> avg = Averager()
    >>> avg(10)
    10.0
    >>> avg(11)
    10.5
    >>> avg(12)
    11.0
    """
    def __init__(self):
        self.series = []
    def __call__(self, new_value):
        self.series.append(new_value)
        total = sum(self.series)
        return total/len(self.series)
```

一个函数的实现方法如下

```
def make_averager():
    """
    >>> avg = make_averager()
    >>> avg(10)
    10.0
    >>> avg(11)
    10.5
    >>> avg(12)
    11.0
    """
    series = []
    def averager(new_value):
        series.append(new_value)
        total = sum(series)
        return total/len(series)
    return averager
```

这里需要注意的是series相对于averager是一个自由变量，也就是这个变量不属于局部变量。

```
>>> avg.__code__.co_varnames ('new_value', 'total')
>>> avg.__code__.co_freevars ('series',)
```
而每一个`avg.__code__.co_freevars`里的变量的值都保存在`avg.__closure__`中，其值在`avg.__closure__[0].cell_contents`

```
>>> avg.__code__.co_freevars
('series',)
>>> avg.__closure__
(<cell at 0x107a44f78: list object at 0x107a91a48>,) 
>>> avg.__closure__[0].cell_contents
[10, 11, 12]
```

所以，闭包就是一个可以从自由变量里获取变量的函数。

下面看看为什么会引入nonlocal这个关键字，以及它的作用。

如果我们想办法消除series变量，可以编写如下函数。

```
def make_averager():
 
    count = 0
    total = 0
    def averager(new_value):
        count += 1
        total += new_value
        return total / count
    return averager
```

但函数执行时会报错

``` 
>>> avg = make_averager()
>>> avg(10)
Traceback (most recent call last):
...
UnboundLocalError: local variable 'count' referenced before assignment
>>>
```

这是因为变量作用域的原因。`count += 1`相当于`count = count + 1`, 此时count会被当做局部变量，而不是引用外面一层的count, 而averager函数里并没有声明count变量，于是报错。可以参看[Python之dis模块](http://program.dengshilong.org/2017/03/02/Python%E4%B9%8Bdis%E6%A8%A1%E5%9D%97/)

在Python3里添加了nonlocal来解决这个问题。

```
def make_averager():
    """
    >>> avg = make_averager()
    >>> avg(10)
    10.0
    >>> avg(11)
    10.5
    >>> avg(12)
    11.0
    """
    count = 0
    total = 0
    def averager(new_value):
        nonlocal count, total
        count += 1
        total += new_value
        return total / count
    return averager
```

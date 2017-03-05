title: Python之装饰器
date: 2017-03-05 13:33:11
tags:
    - Python
    - 装饰器
categories:
---
## 什么是装饰器
在《Fluent Python》里说， A decorator is a callable that takes another function as argument。也就是装饰器就是一个可执行对象，它的参数是一个函数。


```
@decorate
def target():
    print('running target()')
```

相当于

```
def target():
    print('running target()')
target = decorate(target)
```

另一个重要的问题是当模块导入时，装饰器就执行了。

编写registration.py

```
registry = []


def register(func):
    print('running register(%s)' % func)
    registry.append(func)
    return func


@register
def f1():
    print('running f1()')


@register
def f2():
    print('running f2()')


def f3():
    print('running f3()')


def main():
    print('running main()')
    print('registry ->', registry)
    f1()
    f2()
    f3()

if __name__ == '__main__':
    main()
```
之后导入模块，可以看到registration.registry的值

```
>>> import registration
running register(<function f1 at 0x10063b1e0>) 
running register(<function f2 at 0x10063b268>)
>>> registration.registry
[<function f1 at 0x10063b1e0>, <function f2 at 0x10063b268>]
```

## 编写一个装饰器

下面编写一个记录函数执行时间的装饰器，保存到clockdeco.py中

```
import time
def clock(func):
    def clocked(*args): #
        t0 = time.perf_counter()
        result = func(*args) #
        elapsed = time.perf_counter() - t0
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        return result
    return clocked
```
之后使用这个装饰器

```
import time
from clockdeco import clock
@clock
def snooze(seconds):
    time.sleep(seconds)

@clock
def factorial(n):
    return 1 if n < 2 else n*factorial(n-1)

if __name__=='__main__':
    print('*' * 40, 'Calling snooze(.123)')
    snooze(.123)
    print('*' * 40, 'Calling factorial(6)')
    print('6! =', factorial(6))
```
可以看到结果

```
**************************************** Calling snooze(123) [0.12405610s] snooze(.123) -> None **************************************** Calling factorial(6) [0.00000191s] factorial(1) -> 1
[0.00004911s] factorial(2) -> 2
[0.00008488s] factorial(3) -> 6
[0.00013208s] factorial(4) -> 24
[0.00019193s] factorial(5) -> 120
[0.00026107s] factorial(6) -> 720
6!=720
```
### 使用内置装饰器
上面编写的clock装饰器存在一个问题是不支持关键字参数，可以使用标准库里的functools.wraps来解决这个问题。

```
import time
import functools
def clock(func):
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - t0
        name = func.__name__
        arg_lst = []
        if args:
            arg_lst.append(', '.join(repr(arg) for arg in args))
        if kwargs:
        pairs = ['%s=%r' % (k, w) for k, w in sorted(kwargs.items())]
        arg_lst.append(', '.join(pairs))
        arg_str = ', '.join(arg_lst)
        print('[%0.8fs] %s(%s) -> %r ' % (elapsed, name, arg_str, result))
        return result
    return clocked
```

Python内置了三个常用的装饰器，property，classmethod和staticmethod，
标准库functools里还有两个有趣的装饰器lru_cache和singledispatch。

### 编写带参数的装饰器
要编写带参数的装饰器，一个解决的办法是编写一个装饰器工厂，然后根据参数不同，返回不同的装饰器。

拿上面的clock装饰器来说，如果要允许传入时间格式来输出不同的日期格式，可以如下编写装饰器工厂, 保存到clockdeco_param.py中

```
import time
DEFAULT_FMT = '[{elapsed:0.8f}s] {name}({args}) -> {result}'
def clock(fmt=DEFAULT_FMT):
    def decorate(func):
        def clocked(*_args):
            t0 = time.time()
            _result = func(*_args)
            elapsed = time.time() - t0
            name = func.__name__
            args = ', '.join(repr(arg) for arg in _args)
            result = repr(_result)
            print(fmt.format(**locals()))
            return _result
        return clocked
    return decorate
```
编写如下测试代码，可以看到不同的时间格式。

```
import time
from clockdeco_param import clock
@clock()
def snooze(seconds):
    time.sleep(seconds)

for i in range(3):
    snooze(.123)


@clock('{name}({args}) dt={elapsed:0.3f}s')
def snooze(seconds):
    time.sleep(seconds)


for i in range(3):
    snooze(.123)
```
输出结果如下

```
[0.12581110s] snooze(0.123) -> None
[0.12463617s] snooze(0.123) -> None
[0.12825012s] snooze(0.123) -> None
snooze(0.123) dt=0.127s
snooze(0.123) dt=0.126s
snooze(0.123) dt=0.126s
```

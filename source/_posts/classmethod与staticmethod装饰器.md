title: classmethod与staticmethod装饰器
date: 2017-05-06 15:53:48
tags:
    - Python
categories:
---
用classmethod装饰器修饰的函数，第一个参数是类，classmethod的最常见用途是类构造方法

staticmethod实际上并没什么用，使用函数就可以完成相应的功能。

编写如下代码
```
class Demo(object):
    @classmethod
    def klassmeth(*args):
        return args # ... @staticmethod

    def statmeth(*args):
        return args #

if __name__ == "__main__":
    print(Demo.klassmeth())
    print(Demo.klassmeth('spam'))
    print(Demo.statmeth())
    print(Demo.statmeth('spam'))
```
输出结果如下
```
(<class '__main__.Demo'>,)
(<class '__main__.Demo'>, 'spam')
()
('spam',)
```

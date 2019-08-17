title: Python程序设计入门第1讲之递归
date: 2019-08-17 16:39:59
tags:
    - Python
categories:
---
学习了[Python程序设计入门第0讲](https://github.com/dengshilong/learn_python/blob/master/Python%E7%A8%8B%E5%BA%8F%E8%AE%BE%E8%AE%A1%E5%85%A5%E9%97%A8%E7%AC%AC0%E8%AE%B2-%E9%A1%BA%E5%BA%8F%E5%BE%AA%E7%8E%AF%E9%80%89%E6%8B%A9.ipynb)后，对Python有了一定的了解，接下来我们来学习程序设计里一个重要的技巧，那就是递归。

什么是递归呢？简单来说，就是函数自己调用自己，只不过调用参数不同。

一个经典的例子是求正整数的阶乘, 计算某个整数的阶乘，就是求所有小于等于这个数的正整数的和，例如3的阶乘等于6, 5的阶乘等于120。另外还特别规定, 0的阶乘是1

普通的循环写法如下
```
def factorial(n):
    s = 1
    for i in range(1, n + 1):
        s *= i
    return s
print(factorial(1))
print(factorial(3))
print(factorial(5))

1
6
120
40320
```

递归写法如下
```
def factorial(n):
    return n * factorial(n - 1)

print(factorial(3))
```
然而上面的写法会陷入死循环，因为它没有结束条件。加上结束条件后，递归求阶乘如下
```
def factorial(n):
    if n == 1 or n == 0:
        return 1
    return n * factorial(n - 1)

print(factorial(0))
print(factorial(3))
print(factorial(5))
1
6
120
```
如此我们知道递归程序的一个重要条件是要有结束条件

斐波那契数列指的是这样一个数列 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, ........, 写成公式就是 F(1)=1，F(2)=1, F(n)=F(n-1)+F(n-2)（n>=3)

接下来我们用写一个递归程序来计算斐波那契数列
```
def fibonacci(n):
    if n == 1 or n == 2:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)

for i in range(1, 10):
    print(i, fibonacci(i))
    
1 1
2 1
3 2
4 3
5 5
6 8
7 13
8 21
9 34
```
如果仔细观察上面的fibonacci函数，会发现很多计算会重复了，例如求fibonacci(5)时，会计算fibonacci(4)和fibonacci(3), 而求fibonacci(4)时会计算fibonacci(3)和fibonacci(2), 这里fibonacci(3)就会重复计算了，这就导致这个递归函数会特别慢，下面我们测试下fibonacci(35)的速度, 可以看到计算fibonacci(35)差不多要2.82s，这是无法接受的，这种情况可以写成非递归的fibonacci函数

```
def fibonacci(n):
    a = 1
    b = 1
    i = 2
    while i < n:
        c = a + b
        a = b
        b = c
        i += 1
    return b
    
    
for i in range(1, 10):
    print(i, fibonacci(i))

1 1
2 1
3 2
4 3
5 5
6 8
7 13
8 21
9 34
```
此时再计算fibonacci(35)就会很快了

既然递归算法的执行效率不高，那为什么还要用递归？这是因为，一些很难的问题，有时候用递归会变得很简单。一个经典的例子是Hanoi塔问题

汉诺塔(Towers of Hanoi)是一个在入门书籍中常见的例题或习题, 它是说: 有3根柱子, 1、2与3,在柱子1上串了从上到下编号是1, 2, …, m的圆片, 号码小的圆片也小. 问题是, 请写一个程序, 把柱子1上的圆片搬到柱子3去。在搬的时候有3个要求: 第一, 每次只能搬一个圆片; 第二, 要搬的圆片得从某个柱子取出, 并且放到另一根柱子上; 第三, 任何时刻、任何柱子上的圆片, 从上到下都是从小到大排列。

要写出一个非递归算法，是相当有挑战的，而用递归的话，却非常容易。
```
def hanoi_tower(n):
    return _hanoi_tower(n, 1, 2, 3)


def _hanoi_tower(n, start, mid, end):
    """
    把n块圆片从start柱子，借助mid柱子, 搬到end柱子
    """
    if n == 1:
        print("Move disk %d from %d to %d" % (n, start, end))
    else:
        _hanoi_tower(n - 1, start, end, mid)
        print("Move disk %d from %d to %d" % (n, start, end))
        _hanoi_tower(n - 1, mid, start, end)
        
hanoi_tower(3)

Move disk 1 from 1 to 3
Move disk 2 from 1 to 2
Move disk 1 from 3 to 2
Move disk 3 from 1 to 3
Move disk 1 from 2 to 1
Move disk 2 from 2 to 3
Move disk 1 from 1 to 3
```

总的来说，递归算法要满足以下两个条件

1. 要有结束条件，像factorial和fibonacci中的两个if判断
2. 递归的规模要越来越小，像factorial中，求factorial(n)是通过factorial(n-1)得到，fibonacci中求fibonacci(n)是通过求fibonacci(n-1)和fibonacci(n-2)得到，这里传入递归函数的参数都越来越小。

掌握了递归，就掌握了程序设计里非常强大武器之一。

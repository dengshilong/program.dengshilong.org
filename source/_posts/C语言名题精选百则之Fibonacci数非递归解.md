title: C语言名题精选百则之Fibonacci数非递归解
date: 2019-04-03 08:17:23
tags:
    - C名题百则
categories:
---
Fibonacci数列f(1),f(2),...,f(n)的定义是:

1. f(n) = 1 当 n = 1或n = 2时
2. f(n) = f(n-1) + f(n-2) 当n > 2时

不用递归的方法, 也不用数组, 编写一个函数, 它接收n的值, 返回f(n)。

说明: 用递归方法算 Fibonacci数列效率是很低的, 要计算很多个重复的加法, 这个题目要求不用递归, 不用数组, 把f(n)求出来。 不过应注意下面的事项:

1. 递归方式并非全然不好,但不能直接套用公式。
2. 因为当n > 2时,f(n) = f(n-1) + f(n-2),所以程序只保留f(n-1)与f(n-2)就可以算出f(n)。

解答见[iteration_fibonacci.py](https://github.com/dengshilong/C100Problem/blob/master/chapter2/iteration_fibonacci.py)

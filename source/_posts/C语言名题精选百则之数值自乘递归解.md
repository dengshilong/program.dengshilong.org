title: C语言名题精选百则之数值自乘递归解
date: 2019-03-22 22:40:30
tags:
    - C名题百则
categories:
---
如果n与m是正整数, 那么m ^ n 就是把m连乘n次, 这是一个效率很低的方法，请写一个计算效率高的程序 ，并且分析城中一共用了多少个乘法，应该以n - 1个乘法作为设计准则。

说明: 这是一个典型的递归设计题目，应该注意一下几点

1. 试用分而治之(Divide and Conquere)的策略
2. 注意到x ^ 4可以用x ^ 2自乘的关系，由此可以大量地降低乘法数目
3. 连乘n次要n - 1个乘法，能做到只要2log(n)个乘法吗？

解答见[recursion_power.py](https://github.com/dengshilong/C100Problem/blob/master/chapter2/recursion_power.py)

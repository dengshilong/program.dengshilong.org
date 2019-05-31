title: C语言名题精选百则之产生Gray码
date: 2019-05-31 21:34:17
tags:
    - C名题百则
categories:
---
编写一个程序, 用Gray码(Gray Code)的顺序列出一个集合的所有子集。
说明: 这个问题其实是在看有没有办法把Gray(人名)码用程序编写出来, 有了Gray码，找出对应的集合是件简单的事。

什么是Gray码? nbit的Gray码是一连串共有2 ** n 个元素的数列, 每一个元素都有能nbit, 而且任何相邻的两个元素之间只有1的值不同, 例如,3个bit的Gray码:

> 000 001 011 010 110 111 101 100

是一组Gray码, 任何相邻两个元素都只有1bit值不同。但是，Gray码却并不是惟一的，把它循环排列或是用反过来的顺序写,也会得到一组Gray码; 比如说, 如果把最后3个素放到最前面去, 就会得到

> 111 101 100 000 001 011 010 110

也是一组Gray码。

产生Gray码的方法很多，这里这介绍其中一种。
将2bit Gray码列出
00
01
11
10
将3bit Gray码列出
000
001
011
010
110
111
101
100
观察3bit Gray码可以发现，它可以由2bit Gray码来得到。

解答见[gray_code.py](https://github.com/dengshilong/C100Problem/blob/master/chapter3/gray_code.py)

title: C语言名题精选百则之因子分解
date: 2019-03-22 22:12:51
tags:
    - C名题百则
categories:
---
编写一个程序, 读入一个正整数, 把它的所有质因子找出来。例如, 如果输入的是72 = (2 ^ 3) * (3 ^ 2),于是质因子就有 2 与 3, 如果输入的是181944, 181944 = (2 ^ 3) * (3 ^ 2) * 7 * (19 ^ 2), 因子为2、3、7与19。为了方便起见,(2 ^ 3) * (3 ^ 2) * 7 * (19 ^ 2)可以用2(3)3(2)7(1)19(2)作为输出形式, 也就是说,如果分解开来有a ^ b,输出时就是a(b)。

说明: 传统的做法是把输入值(假设是n)用2去除,一直到除不尽为止。如果一共除了i次就有2 ^ i这一项,输出中就会出现2(i); 接着再用3去除、5去除、7去除等,直到商数变成1为止。以181944为例,第一次用2除得到93972, 再除一次是46896, 第三次得到23493,于是2就不能整除了。下来用3去除, 第一次得到7831, 第二次是2527, 第三次就不能整除。对于2527而言, 用7去除得到361, 再用7就除不尽了, 其次的11、13、15、17也都除不尽; 但19可以, 再用19去除得19; 最后用19除, 商为1, 不能再除了,因此就得到181944 = (2 ^ 3) * (3 ^ 2) * 7 * (19 ^ 2)的结果。试用这个概念来编写程序。

解答见[factor.py](https://github.com/dengshilong/C100Problem/blob/master/chapter2/factor.py)

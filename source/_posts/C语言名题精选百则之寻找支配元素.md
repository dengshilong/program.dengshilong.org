title: C语言名题精选百则之寻找支配元素
date: 2019-06-16 20:13:03
tags:
    - C名题百则
categories:
---
已知一个整数数组x, 对于任何一个元素x[i]而言, 在x[i]右边, 而且值不比x[i]小的元素(亦即j > i而且x[j] >= x[i]的x[j])都叫做x[i]的右支配元素(Right Dominator). 在x[i]所有的右支配元素中最靠近x[i]的那一个, 就叫做最靠近的右支配元素(Right Nearest Dominator). 当然, 不见得每一个元素都有支配元素的, 如最大元素就没有,问题是, 编写一个程序, 接收一个数组, 把数组中每一个元素最靠近的右支配元素找出来

说明: 看个例子比较容易明了这个问题的要求。如果数组的内容是2, 1, 3, 5, 4那么3, 5, 4都是2的右支配元素, 但3是最靠近的一个, 所以3是2的最靠近右支配元素, 同理1与3的最靠近右支配元素分别是3与5, 5与4都没有最靠近右支配元素; 对5而言, 右边没有元素比它大;就4而言, 右边没有元素了。

看起来程序并不难写,因为可以x[1], x[2] …, x[i],…一个接一个查过去; 当查到x[i]时，就查x[i+1], x[i+2]…, 于是第一次找出比x[i]大或相等的元素, 就是x[i]的最靠近右支配元素了。但是这样的做法效率并不高。举例而言, 如果一个数组的元素是从大到小排好的但是最后一个元素是整个数组的极大值(例如,5, 4, 3, 2, 1, 6)。若数组有n个元素, 处理x[0]要比较n-1次, 处理x[1]时比较n-2次, 一般而言, 处理x[i]时要比较n - i次。所以就一共用了(n-1) + (n-2) + … + 3 + 2 + 1 =n (n-1)/2, 差不多是n ** 2次的比较.

因此, 挑战是, 能不能写出比较次数与n成正比的程序?

参考文献: 这个题目与解法来自 Hubert Wagener在1988年的一篇文章。Wagener是用这个观点来决一个计算几何(Computational Geometry)中的重要问题, 不过他的重点是平行式的算法,但是他的文章中两个解法都有。有兴趣的朋友可以参看

H Wagener. Triangulating a Monotone Polygon in Parallel. Computational Geometry and Its Applications, Lecture Notes in Computer Science, No 333, Springer-Verlag. 1988, Pp 136-147

解答见[dominator.py](https://github.com/dengshilong/C100Problem/blob/master/chapter9/dominator.py)

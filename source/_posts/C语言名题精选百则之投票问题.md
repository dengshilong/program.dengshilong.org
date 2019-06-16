title: C语言名题精选百则之投票问题
date: 2019-06-16 15:20:38
tags:
    - C名题百则
categories:
---
这个问题一般叫做过半数(Majority)问题, 也有人称为投票(Voting)问题, 但以前者说法居多。假设有1, 2, ... n等n个人参加投票, 他们只能圈选一个人, 但是却可以选任何一人, 甚至于可以选不在这n个人中的另一个都行。例如, 如果5个人投票, 分别投1、8、1、100、1; 1、3、5都投给1, 2投给8, 4投给100。问题是, 写一个程序接收这些投票结果, 看看有没有人的得票过半数, 就以上例来看, 1的得票数就过半数了.

说明: 这是个名题, 也与其他问题一样有简单但效率低的解法, 但也有较有技巧且效率高的做法, 简单做法是, 把投票结果先从小到大排好, 把投给同一个人的票就收在一起, 接着从头查起, 看看一连串相同的值的个数, 如果有过半数的, 那个人就当选了。用上面的例来看, 从小到大排好是1, 1, 1, 8, 100, 很显然1有3个, 过半数了, 因此1会当选。

这是一个大家都会想到的想法, 但事实上, 排大小的这一步是不必要的, 能开发出这样的程序吗? 不过要记住一点, 不能对候选人的数目作任何假设, 因为如果假定候选人是1, 2, …, k, 那么这个题目就简单至极而不会变成名题了。为什么呢? 准备一个有k个元素的
数组, 然后……(一定马上就知道是怎么回事了吧!)。

参考文献: 这个题目起源于容错(Fault Tolerant)计算机系统中的一个问题, 是在1981年由 J. Moore(发现匹配字符串的 Boyer-Moore方法的那一个More)提出来的。1982年, J Misra与 David Gies两人合写了一篇深入探讨程序写作的文章, 同年 M.J.Fischer与S. L Salzberg提出了个比此例复杂的方法, 比较1.5n+1次就可以找出结果, 而且还证明了不管用什么办法,比较次数都不可能少于1.5n - 2次。推荐读读上述的文章, 以及所附的文献, 了解问题的来龙去脉。

1. M.J. Fischer and S L Salzberg. Solution to Problem 81-5, Journal of Algorithms, Vol3(1982), pp.375~379
2. Misra and D Gries. Finding Repeated Elements, Science of Computer Programming Vol2(1982), pp.143~152
3. J.Moore. Problem 81-5, Journal of Algorithms. Vol 2(1981), Pp 208-209

解答见[voting.py](https://github.com/dengshilong/C100Problem/blob/master/chapter9/voting.py)

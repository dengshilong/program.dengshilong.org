title: C语言名题精选百则之最大连续元素和
date: 2019-05-10 22:18:00
tags:
    - C名题百则
categories:
---
已知数组x[]储存了一组整数, 请写一个程序, 找出在数组中连续元素的和中最大的一个。举例而言, 如果有数组[1, 2, -6, 3, -2, 4, -1, 3, 2, -4], 那么连续的元素的和有1 + 2 = 3, 1 + 2 + (-6) = 3, 2 + (-6) = 4, ..., 但值最大的就是3 + (-2) + 4 +(-1) + 3 + 2这一段, 值为9. 规定: 和为负值时就定成0, 所以结果永远不为负。这个题目通常叫做最大连续元素和(Maximum Consecutive Sum)问题

说明: 这个问题有个很简单的解法,但效率很低,一般采用效率很高的方法的程序比使用不好的方法的要长。一般人看到这个问题的自然反应就是用两个循环, 如程序所示。

```
def bad_method(x):
    max_sum = 0
    for i in range(len(x)):
        s = 0
        for j in range(i, 0, -1):
            s += x[j]
            if s > max_sum:
                max_sum = s
    return max_sum
```

想法是很简单的, 当固定在某个x[i]之后, 把x[i], x[i-1] + x[i], x[i-2] + x[i-1] + x[i], ... x[0] + x[1] + ... x[i]求出来, 一边算, 一边找出极大值, 这就是上面片段所隐含的意义。但是, 当处理到i时要查i个元素, 所以要把n个数都处理完,就要查1 + 2 + 3 + … + i + ... + n = n(n+1)2、与n ** 2成正比的元素了。如果仔细看就会发现做了很多重复的工作, 为什么? 当i是2时,算了x[2], x[1] + x[2], x[0] + x[1] + x[2], 但当i进到下一个位置变成3时, 又算x[3], x[2] + x[3], x[1] + x[2] + x[3], x[O] + x[1] + x[2] + x[3], 于是x[1] + x[2] 与 x[O] + x[1] + x[2]不都是重复算了吗? 因此, 程序如果能够避免这些重复的部分, 就一定会非常快。

解答见[maximum_consecutive_sum.py](https://github.com/dengshilong/C100Problem/blob/master/chapter9/maximum_consecutive_sum.py)

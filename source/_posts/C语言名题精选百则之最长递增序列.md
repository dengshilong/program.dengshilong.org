title: C语言名题精选百则之最长递增序列
date: 2019-06-10 20:46:41
tags:
    - C名题百则
categories:
---
已知一个整数数组, 在这个数组中的一个递增序列, 就是把若干元素删除后所留下的元素按从小到大的顺序排列。举例而言, 如果数组是1,3,5,7,8,2,9,4,10,6, 那么1,5,8,9,10是个递增序列, 3,5,8,9,10也是一个递增序列, 1,3,5,7,9,10 也是递增序列。简单地说, 可以依数组元素的次序选出若干元素, 使得从小到大排好 ,那么这就是个递增序列。例如3,8; 2,9; 7,10; 2,4,6; …。但是9,4,10; 5,7,8,2,9等却不是递增序列。 问题是, 写一个程序接收一个整数数组, 找出这个数组中最长的递增序列的长度。以上面的例子来看, 1,3,5,7,8,9,10是最长的递增序列, 所以程序输出7的结果。

说明: 递增序列的意义已如上述, 程序要如何写? 看起来似乎很难下手, 但总是有迹可寻的,为什么呢? 递增序列不会凭空出现, 一定是先有了几个, 然后又出现一个新元素, 看看这个新元素能不能加到已有的递增序列后面, 如果可以,已有的递增序列的长度就多了1; 但若不能添加, 那要做些什么事呢? 那就要自己想了. 先看个例子, 还是以1,2,4,3,6为例。假设目前已经发现了如下的几个递增序列:
> 1,2,4,6(长度为4)
> 
> 1,2,3(长度为3)

现在新来的元素是5, 因此5可以补在1,2,3后面而得到1,2,3,5(长度为4); 那么5对1,2,4,6的关系又如何? 这就要自己想了。

这个问题的起源可能是组合数学(Combinatoric Mathematics)。组合数学中有一个定理, 它说n ** 2 + 1个数中一定有一个长度至少为n的递增或递降序列。此处不过是要求写一个程序把最长的递增序列的长度找出来而已, 会写这个程序之后, 递降序列也不过是同一回事。

解答见[longest_increase_sequence.py](https://github.com/dengshilong/C100Problem/blob/master/chapter9/longest_increase_sequence.py)

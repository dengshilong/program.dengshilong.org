title: C语言名题百则精选之寻找脚码
date: 2019-04-27 21:07:06
tags:
    - C名题百则
categories:
---
已知一个整数数组x[], 其中的元素彼此都不相同,而且也已经从小到大排列好,请用
比较大小、相等的方式编写一个程序, 找出给定的数组中是否存在一个元素满足x[i] = i的关
系。举例而言, 如果x[]={-2,-1,3,7,8}, x[3] = 3, 因此 3 就是答案, 因为编程语言中数组是从0开始的，所以最终是检测是否存在一个元素满足x[i] = i + 1.

说明: 用笨方法, 一个循环就可以找出答案, 如下程序所示

```
def bad_index_search(x):
    index = -1
    for i in range(0, len(x)):
        if x[i] == i + 1:
            index = i + 1
            break
    return index

if __name__ == "__main__":
    x = [-2, -1, 3, 7, 8]
    print(bad_index_search(x))
```

这个程序在最坏的情况下, for一共绕了n圈, 作了n次比较, 但却没有用到x[]的元
素已经排列好的条件. 事实上, 如果输入有n个元素, 应该可以写出与log(n)次成正比的比较的程序,关键是x[]的元素是排好顺序的。

解答见[index_search.py](https://github.com/dengshilong/C100Problem/blob/master/chapter4/index_search.py)

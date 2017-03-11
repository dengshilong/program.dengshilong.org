title: Python元祖谜题
date: 2017-03-11 15:46:11
tags:
    - Python
    - 元祖
categories:
---
这是一道关于元祖+=赋值的谜题, 据说，能答对这道题的都是Python老司机。 请在不执行下面的代码的情况下，回答这个问题

```
>>> t = (1,2,[30,40])
>>> t[2] += [50, 60]
会发生什么, 选择最佳答案:
a) t变成(1, 2, [30, 40, 50, 60])
b 抛出TypeError, 'tuple' object does not support item assignment异常，即元祖对象不支持赋值
c) 上面两种情况都没有发生.
d) a 和 b都发生
```

看到这题时，第一反应是b。之后使用dis模块查看执行语句, 得到

```
>>> dis.dis("t[2] += [50, 60]")
  1           0 LOAD_NAME                0 (t)
              3 LOAD_CONST               0 (2)
              6 DUP_TOP_TWO
              7 BINARY_SUBSCR
              8 LOAD_CONST               1 (50)
             11 LOAD_CONST               2 (60)
             14 BUILD_LIST               2
             17 INPLACE_ADD
             18 ROT_THREE
             19 STORE_SUBSCR
             20 LOAD_CONST               3 (None)
             23 RETURN_VALUE
```
可以看到第17条的INPLACE_ADD操作，因为列表是可变对象，所以这条会执行成功。之后第19条进行保存，而元祖是不可变对象，所以第19条会报错。

所以答案是d, 即a和b都发生了。

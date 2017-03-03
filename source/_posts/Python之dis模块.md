title: Python之dis模块
date: 2017-03-02 14:29:00
tags:
    - Python
    - dis
categories:
---
[dis](https://docs.python.org/3/library/dis.html), 即Disassembler for Python bytecode, 用于Python字节码的反汇编。可以用于查看函数的具体执行步骤，例如下面的局部变量的例子

```
def f1(a):
    print(a)
    print(b)
```
得到

```
  3           0 LOAD_GLOBAL              0 (print)
              3 LOAD_FAST                0 (a)
              6 CALL_FUNCTION            1 (1 positional, 0 keyword pair)
              9 POP_TOP

  4          10 LOAD_GLOBAL              0 (print)
             13 LOAD_GLOBAL              1 (b)
             16 CALL_FUNCTION            1 (1 positional, 0 keyword pair)
             19 POP_TOP
             20 LOAD_CONST               0 (None)
             23 RETURN_VALUE
```

执行

```
a = 3
b = 4
f1(a)
```
不会报错，这里第13条是LOAD_GLOBAL，此时有全局变量b.

再看这个例子

```
def f2(a):
    print(a)
    print(b)
    b=9
```
得到的是

```
  4           0 LOAD_GLOBAL              0 (print)
              3 LOAD_FAST                0 (a)
              6 CALL_FUNCTION            1 (1 positional, 0 keyword pair)
              9 POP_TOP

  5          10 LOAD_GLOBAL              0 (print)
             13 LOAD_FAST                1 (b)
             16 CALL_FUNCTION            1 (1 positional, 0 keyword pair)
             19 POP_TOP

  6          20 LOAD_CONST               1 (9)
             23 STORE_FAST               1 (b)
             26 LOAD_CONST               0 (None)
             29 RETURN_VALUE
```

执行

```
a = 3
b = 4
f2(a)
```
会报找不到局部变量b, 这是因为第13条LOAD_FAST是加载局部变量，此时还没有局部变量b.

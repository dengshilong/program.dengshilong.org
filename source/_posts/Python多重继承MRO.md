title: Python多重继承MRO
date: 2016-05-10 12:51:51
tags:
    - 多重继承
    - MRO
categories:
    - Python
---
最近在看《Python学习手册》，看到多继承部分，对于函数查找以为使用广度优先，查找[MRO](https://www.python.org/download/releases/2.3/mro/)文档才发现使用C3算法

对于class C(p1, p2, ..., pn), mro(c) = [c] + merge(mro(p1), mro(p2), ..., mro(pn), [p1, p2, ..., pn])

而其中merge的规则是，从左到右选取第一个在列表中是头，在其它列表中不是尾的类，将这个类加入到mro中，并将它从merge中移除，然后继续merge直到结束。如果不能找到这样的头，则无法构造类，将会报错。

举个例子，对于
```
O = object
class F(O): pass
class E(O): pass
class D(O): pass
class C(D,F): pass
class B(E,D): pass
class A(B,C): pass

if __name__ == "__main__":
    print A.mro()
```
查找顺序是
```
[<class '__main__.A'>, <class '__main__.B'>, <class '__main__.E'>, <class '__main__.C'>, <class '__main__.D'>, <class '__main__.F'>, <type 'object'>]
```
计算过程如下
```
mro(F) = [F, O]
mro(E) = [E, O]
mro(D) = [D, O]
mro(C) = [C] + merge([D, O], [F, O], [D, F])
       = [C, D] + merge([O], [F, O], [F])
       = [C, D, F] + merge([O], [O])
       = [C, D, F, O]
mro(B) = [B] + merge([E, O], [D, O], [E, D])
       = [B, E] + merge([O], [D, O], [D])
       = [B, E, D] + merge([O], [O])
       = [B, E, D, O]
mro(A) = [A] + merge([B, E, D, O], [C, D, F, O], [B, C])
       = [A, B] + merge([E, D, O], [C, D, F, O], [C])
       = [A, B, E] + merge([D, O], [C, D, F, O], [C])
       = [A, B, E, C] + merge([D, O], [D, F, O])
       = [A, B, E, C, D] + merge([O], [F, O])
       = [A, B, E, C, D, F] + merge([O], [O])
       = [A, B, E, C, D, F, O]
```

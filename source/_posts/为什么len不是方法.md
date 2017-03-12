title: 为什么len不是方法
date: 2017-03-12 17:58:06
tags:
    - Python
categories:
---
在《Fluent Python》里看到Why len is not method，有些困惑，于是开始找答案。

在Python词汇表里，对函数和方法有如下说明
[function](https://docs.python.org/3/glossary.html#term-function): A series of statements which returns some value to a caller. It can also be passed zero or more arguments which may be used in the execution of the body.

[method](https://docs.python.org/3/glossary.html#term-method): A function which is defined inside a class body. If called as an attribute of an instance of that class, the method will get the instance object as its first argument (which is usually called self). 

简单来说，就是函数在类里定义就叫方法。所以这里len是一个函数，而不是方法。那么问题是，为什么不把len做成方法，像list.len() str.len()这样呢？

在[What makes Python so AWESOME](https://www.youtube.com/watch?v=NfngrdLv9ZQ)里《Fluent Python》的作者Luciano Ramalho向Raymond Hettinger提了这个问题，Raymond Hettinger说是因为"practicality beats purity", 因为把len做成一个函数更加直观和符合直觉。

实际实现时，len函数对于内置类型，会去C底层实现的结构体里取一个字段值，这个字段值记录了长度。而对于用户自定义类型，用户实现__len__方法的话，len函数会去调用__len__方法。

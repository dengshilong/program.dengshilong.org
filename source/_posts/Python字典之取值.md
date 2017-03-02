title: Python字典之取值
date: 2017-03-02 10:56:05
tags:
    - Python
    - dict
categories:
---
在使用Python字典时，有两种方式，d[key]与d.get(key)，它们有一些细微的区别

* d[key]底层实现是调用`dict.__getitem__`, 而d.get(key)就是一个函数调用。

* 当`dict.__getitem__` 没有找到key时，会调用`dict.__missing__`

编写测试代码如下
```
class Dict(dict):
    def __getitem__(self, key):
        return 2

class TestMiss(dict):
    def __missing__(self, key):
        return 3

if __name__ == "__main__":
    d = Dict()
    d["key"] = "test"
    print(d.get("key"), d["key"], d.get("k"), d["k"])

    d = TestMiss()
    d["key"] = "test"
    print(d.get("key"), d["key"], d.get("k"), d["k"])
```
输出结果如下
```
test 2 None 2
test test None 3
```

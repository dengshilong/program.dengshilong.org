title: Python字典之取值
date: 2017-03-02 10:56:05
tags:
    - Python
    - dict
categories:
---
《Fluent Python》中写到，在使用Python字典时，有两种方式，d[key]与d.get(key)，它们有一些细微的区别

* d[key]底层实现是调用`dict.__getitem__`, 而d.get(key)就是一个函数调用。

* 当`dict.__getitem__` 没有找到key时，会调用`dict.__missing__`

执行如下代码
```
from dis import dis
d = dict()
print(dis('d["a"]'))
print(dis('d.get("a")'))
```

输出如下结果

```
 1           0 LOAD_NAME                0 (d)
              3 LOAD_CONST               0 ('a')
              6 BINARY_SUBSCR
              7 RETURN_VALUE
None
  1           0 LOAD_NAME                0 (d)
              3 LOAD_ATTR                1 (get)
              6 LOAD_CONST               0 ('a')
              9 CALL_FUNCTION            1 (1 positional, 0 keyword pair)
             12 RETURN_VALUE
```
可以看到get是函数调用，而d[]不是。

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

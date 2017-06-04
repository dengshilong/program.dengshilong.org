title: Python之attribute与property
date: 2017-06-04 20:34:09
tags:
    - Python
    - property
categories:
---
在Python中property是一个常用的装饰器，一个常用的用途是将方法变成属性访问。另一个需要注意的是，使用它可以改变对象中属性的访问顺序。

编写如下测试类

```
class Class:
    data = 'the class data attr'

    @property
    def prop(self):
        return 'the prop value'
```

然后在交互环境下测试如下
```
>>> obj = Class()
>>> vars(obj) #
{}
>>> obj.data #
'the class data attr'
>>> obj.data = 'bar' #
>>> vars(obj) #
{'data': 'bar'}
>>> obj.data #
'bar'
>>> Class.data #
'the class data attr'
```
可以看到在obj.data = 'bar'后，对象中的data覆盖了类中的data

当对于proptery，对象中的attribute无法覆盖类中的attribute，在交互条件下输入如下操作可以看到结果
```
>>> Class.prop #
<property object at 0x1072b7408>
>>> obj.prop #
'the prop value'
>>> obj.prop = 'foo' #
Traceback (most recent call last):
...
AttributeError: can't set attribute
>>> obj.__dict__['prop'] = 'foo' #
>>> vars(obj) #
{'prop': 'foo', 'data': 'bar'}
>>> obj.prop #
'the prop value'
>>> Class.prop = 'baz' #
>>> obj.prop #
'foo'
```
在对象中，obj.prop = 'foo'这个操作会报错，这是因为property会覆盖对象的属性，而此时prop还未实现set方法。即便是通过obj.__dict__设置了prop属性，obj.prop获取到的依然是类中的prop


也就是property会覆盖对象的属性，看下面的例子就很清楚了
```
>>> obj.data #
'bar'
>>> Class.data #
'the class data attr'
>>> Class.data = property(lambda self: 'the "data" prop value') #
>>> obj.data #
'the "data" prop value'
>>> del Class.data #
>>> obj.data #
'bar'
```

在类属性data变成了property后，即` Class.data = property(lambda self: 'the "data" prop value') #`, 对象中的data的读取也跟着改变了。

简单来说，就是对象中的属性会覆盖类中的属性，而类中的property会覆盖对象中的属性。同样的，类中的descriptor也会覆盖对象中的属性。

## 参考资料
* [Attributes, Properties and Descriptors](http://www.itmaybeahack.com/book/python-2.6/html/p03/p03c05_properties.html)
* 《Fluent Python》第19章

title: Object.freeze在JavaScript逆向时的妙用
date: 2025-09-21 19:10:55
tags:
    - JavaScript
    - 逆向
categories:
---
在 JavaScript 逆向时，有时候反爬代码会对console进行更改，导致使用 console.log 输出时没有结果，如下面的例子

```
console.log = function log(t) {
}
console.log('ssss')
```

这时我们可以使用 Object.freeze 方法把 console 冻结了，不让它更改，这样就会有输出了，例子如下

```
Object.freeze(console)
console.log = function log(t) {
}
console.log('ssss')
```

在MDN文档里可以看到，Object.freeze() 静态方法可以使一个对象被冻结。冻结对象可以防止扩展，并使现有的属性不可写入和不可配置。被冻结的对象不能再被更改：不能添加新的属性，不能移除现有的属性，不能更改它们的可枚举性、可配置性、可写性或值，对象的原型也不能被重新指定。freeze() 返回与传入的对象相同的对象。

当然反爬也可以使用 Object.isFrozen() 方法查看 console 是否被冻结, 发现被冻结了，就知道大概率是爬虫了，因为正常用户谁会好端端的冻结 console 呢？

### 参考资料:

https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Object/freeze

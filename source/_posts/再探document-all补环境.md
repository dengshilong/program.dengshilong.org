title: 再探document.all补环境
date: 2025-03-28 19:54:01
tags:
    - Node
    - 爬虫
    - 补环境
    - 逆向
    - JavaScript
categories:
---
在[JavaScript逆向时一些奇奇怪怪的检测](http://program.robinjia.cc/2025/03/21/JavaScript%E9%80%86%E5%90%91%E6%97%B6%E4%B8%80%E4%BA%9B%E5%A5%87%E5%A5%87%E6%80%AA%E6%80%AA%E7%9A%84%E6%A3%80%E6%B5%8B/)里，我们写过一个使用Node v8内置函数来过 document.all 补环境检测的demo, 代码如下

```
const v8 = require("v8");
const vm = require("vm");

// 允许使用 V8 内置函数（需启用 --allow-natives-syntax 标志）
v8.setFlagsFromString('--allow-natives-syntax');

// 创建不可检测对象
let undetectable = vm.runInThisContext('%GetUndetectable()');

// 恢复标志禁用（可选）
v8.setFlagsFromString('--no-allow-natives-syntax');


function HTMLAllCollection() {
    return undetectable
};
Object.defineProperties(HTMLAllCollection.prototype, {
    [Symbol.toStringTag]: {
        value: 'HTMLAllCollection',
        configurable: true
    }
});
undetectable.__proto__ = HTMLAllCollection.prototype;
document = {}
document.all = new HTMLAllCollection()

length = 3;
for (let i = 0; i < length; i++) {
    document.all[i] = '1';
}
debugger;
document.all.length = length;
console.log(typeof document.all)
console.log(document.all)
console.log(document.all.length)
```

有道友说这种检测已经算简单了，可以回去看看document.all(),  测试了下这函数也没啥啊，就返回null,  后来去看了下document.all的特性，才发现它有和form表单一样的特性，例子如下

```
var input = document.createElement('input')
input.name = 'aaa'
document.body.append(input)
input = document.createElement('input')
input.id = 'bbb'
document.body.append(input)
document.all.aaa
document.all('aaa')
document.all.bbb
document.all('bbb')
```

这就令人头秃了。想来安全人员为了兼容还是留了一手了，要不然真的难搞了。以前刚学补环境的时候，就像拿到个锤子，总是锤来锤去，后面锤多了才发现越来越难锤，慢慢就回归到自动化了。毕竟算法，补环境，自动化都是工具，什么好用就用啥了。

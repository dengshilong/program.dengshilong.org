title: JavaScript逆向时一些奇奇怪怪的检测
date: 2025-03-21 19:39:42
tags:
    - JavaScript
    - 逆向
    - 补环境
    - 爬虫
categories:
---
JavaScript逆向时一些奇奇怪怪的检测

之前和同事讨论过一些检测，同事说可以记录下来，能帮到新人，于是有了这篇文章。

# document.all
这是在浏览器里被特殊处理的一个特性，也就是typeof document.all是undefined, 但却document.all却能取到值。要在Node中实现这个特性，现在有两种方案，一种是Node C++插件，另一种是V8内置函数。一般场景用V8内置函数即可，移植性更高。Node C++插件和系统有关，也和Node版本绑定，移植性差。

要实现这个特性，GPT给出如下答案

```
const v8 = require("v8");
const vm = require("vm");

// 允许使用 V8 内置函数（需启用 --allow-natives-syntax 标志）
v8.setFlagsFromString('--allow-natives-syntax');

// 创建不可检测对象
let undetectable = vm.runInThisContext('%GetUndetectable()');

// 恢复标志禁用（可选）
v8.setFlagsFromString('--no-allow-natives-syntax');

// 测试对象行为
undetectable.aaa = 'bbb';
console.log('typeof undetectable:', typeof undetectable);  // 输出 'undefined'
console.log('undetectable.aaa:', undetectable.aaa);       // 输出 'bbb'
console.log('undetectable instanceof Object:', undetectable instanceof Object); // 输出 'true'
```

修修改改，即可实现document.all

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

# eval('!new function(){eval("console.log(this);this.a=2")}().a')

这个主要用来检测vm2环境，在浏览器和Node里都是false,  在vm2里是true, 测试代码如下

```
const { VM } = require("vm2");
const vm = new VM();

vm.run(`
  const obj = new function() {
    eval("console.log(this);this.a=2");
  }();
  console.log(obj);      // 输出空对象 {}
  console.log(obj.a);    // 输出 undefined
  console.log(!obj.a);   // 输出 true
`);
```

# window["Object"]\["getOwnPropertyNames"](Function.prototype.toString)
这个主要考察严格模式和非严格模式, 正常用以下方法重定义

```
Function.prototype.toString  = function toString() {};
console.log(Object.getOwnPropertyNames(Function.prototype.toString));
```
会返回['length', 'name', 'arguments', 'caller', 'prototype']

用以下方法重定义

```
Function.prototype.toString = {toString(){}}.toString
console.log(Object.getOwnPropertyNames(Function.prototype.toString));
```
则返回 ['length', 'name']

# form表单特性

```
let form = document.createElement('form');
form.action = 'https://www.baidu.com/';
let input = document.createElement('input');
input.name = 'action';
form.appendChild(input)
input = document.createElement('input');
input.name = 'textContent';
input.id = 'password';
form.appendChild(input)
console.log(form.action)
console.log(form.textContent)
console.log(form.password)
```
正常form.action是一个url链接，但这里变成了HTMLInputElement。

# 参考资料
零点的 [JavaScript toString 检测对抗](https://mp.weixin.qq.com/s/p_9YDrQwVnDXud1k7aHCXA)


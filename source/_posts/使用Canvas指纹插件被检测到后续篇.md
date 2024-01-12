title: 使用Canvas指纹插件被检测到后续篇
date: 2024-01-12 21:10:36
tags:
    - 补环境
    - JavaScript
    - 指纹
    - 浏览器
categories:
---
上周写完[使用Canvas指纹插件被检测到](http://program.robinjia.cc/2024/01/06/%E4%BD%BF%E7%94%A8Canvas%E6%8C%87%E7%BA%B9%E6%8F%92%E4%BB%B6%E8%A2%AB%E6%A3%80%E6%B5%8B%E5%88%B0/)后，[Nanda佬](https://mp.weixin.qq.com/s/2TT4pSlFUFX965C--R1CJQ)正好看到，提了一句关注下HTMLCanvasElement.prototype.toDataURL.prototype，这个值可能发生变化。

于是对比原始浏览器和重定义toDataURL函数后的 toDataURL ，果然不一样。原先浏览器的 HTMLCanvasElement.prototype.toDataURL.prototype 的值是 undefined , 重定义toDataURL函数后，HTMLCanvasElement.prototype.toDataURL.prototype 的值就变成了函数。加上HTMLCanvasElement.prototype.toDataURL.prototype = undefined 后，网站上就返回了边界数据，也不返回假数据了。

继续测试了几个 toString 后有 native code 字样的函数，如 toString, atob, setTimeout 等等，ChatGPT 的解释是有 native code 意味着该函数的具体实现是由浏览器或 JavaScript 引擎提供的，而不是由 JavaScript 本身的代码编写的，它们的 prototype 都是 undefined 。

这就值得引起注意了，在补环境的时候，对native函数都要引起重视，重定义 native 函数后，要保证它们的 prototype 还是 undefined。打开自己写的补环境框架，测试了几个 native 函数，prototype 都是函数，处理的真垃圾。打开开始佬开源的 [qxvm](https://github.com/ylw00/qxVm), 测试了几个 native 函数， prototype 都是 undefined，处理的真不错。

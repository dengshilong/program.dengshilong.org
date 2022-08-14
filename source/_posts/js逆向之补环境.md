title: js逆向之补环境
date: 2022-08-14 11:21:56
tags:
    - 逆向
    - 补环境
    - js
categories:
---
js代码在Node环境中可以执行，但因为与浏览器环境不一致，生成的参数会与浏览器不同，这时就需要用到补环境，补充Node环境相对于浏览器缺少的环境，去除Node环境中相对于浏览器多余的环境。

例如Node环境中，函数toString的时候大都是function () { [native code] } ，而浏览器中会返回整个函数定义

Node环境中有module, Buffer等等，而浏览器中没有.

还有一些会检测原型链，例如浏览器中document.bod有值，但是document.hasOwnProperty('body')却是false.

补环境的时候，proxy是一个非常有用的工具。固定本地代码和浏览器代码，固定随机参数，慢慢对比。

补环境教程推荐志远的补环境视频，那是真的强。

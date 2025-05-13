title: 再探window.ActiveXObject=undefined
date: 2025-05-13 20:39:12
tags:
    - 爬虫
    - JavaScript
    - 补环境
    - 逆向
categories:
---
之前在[神奇的window.ActiveXObject=undefined](http://program.robinjia.cc/2024/06/29/%E7%A5%9E%E5%A5%87%E7%9A%84window-ActiveXObject-undefined/)里写过，加上window.ActiveXObject=undefined后，某数的校验就降级了，很多环境校验就都没走了。但神奇的是，在我的一个补环境方案里，去掉这行后，很多环境校验一样没走，一样能过反爬，于是我懵，我困惑了，这到底是什么鬼bug啊。

去网上查了下ActiveXObject这个对象，仅支持微软 Internet Explorer 浏览器，在其它现代浏览器（如 Chrome、Firefox、Safari 等）中无法使用，包括微软的 Edge 浏览器(Chromium 内核)也无法使用。也就是说，只有在微软 Internet Explorer 浏览器里，'ActiveXObject' in window才是true, 在其它现代浏览器里，'ActiveXObject' in window 都是false。

而在补环境的时候，userAgent 是Chrome, Edge等浏览器时，如果加上 window.ActiveXObject = undefined; 这行，'ActiveXObject' in window 就会变成true了，就不符合上述的结果，是可以被检测出来的。

很多人补环境不严格，补环境代码里有 window.ActiveXObject = undefined; userAgent是 Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0，这种是Chromium 内核的，换成是我做反爬，就要干它了，悄咪咪的把它记下来，然后在夜深人静的时候给它返回点假数据。

# 参考资料:

https://webaim.org/blog/user-agent-string-history/

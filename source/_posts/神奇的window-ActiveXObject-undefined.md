title: 神奇的window.ActiveXObject=undefined
date: 2024-06-29 22:08:09
tags:
    - 补环境
    - JavaScript
categories:
---

之前在群里就看到有道友在讨论这个问题，但因为没有遇到过这个问题，就没细看，这次自己也遇到了，就认真看了下。

在寻找高效的某数 cookies 生成方案时，看到如画佬星球的补环境方案后，深有感触。最近两年，虽然把补环境框架搞的越来越完善，但同时执行速度也越来越慢，想想似乎有点背离补环境的初衷。上一次yidun的加密生成方案尤其明显，补环境方案把整个CPU都打满了，后面搞了个补环境和扣代码结合的方案后跑的就稳稳的，两者之间性能整整差了10倍。

于是就尝试这种最开始学习的补环境方案，缺啥补啥，争取补的环境每一行代码都是有用的，然后就遇到这个 ActiveXObject 问题了。在 proxy 输出日志中，看到有 ActiveXObject 调用日志，于是在浏览器里看，window.ActiveXObject 就是 undefined, 在Node里，window=global 后，window.ActiveXObject 也是 undefined，于是就没管 ActiveXObject 。但生成的 cookies 就是过不去，只好和如画佬的代码做对比，发现就是因为他的代码有 window.ActiveXObject=undefined，所以能过。

于是去了解 ActiveXObject，发现它是IE才有的对象，在IE中，'ActiveXObject' in window 是true, 而在 Chrome 中 'ActiveXObject' in window 是 false。如果在检测代码中有 'ActiveXObject' in window 这种检测，那么补环境代码中有没有 window.ActiveXObject=undefined 就会影响检测代码执行路径了。在Node中加上 window.ActiveXObject=undefined 后，'ActiveXObject' in window 也就成了 true 了，检测代码就会认为是 IE浏览器，就会按照IE浏览器来检测。手头上方便调试的只有Chome浏览器，就再继续探究后面如何检测的。神奇的是，我是在Mac上用Chrome调试的代码，最后还得伪装成IE才能通过检测，就离谱。

回过头来看代理日志，有针对in操作符的代理has=> [window] 有无属性名 => [ActiveXObject], 结果 => [false] 这行，就是 代理has输出日志，说明检测代码里有 'ActiveXObject' in window 的检测，只是没注意到。


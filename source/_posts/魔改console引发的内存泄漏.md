title: 魔改console引发的内存泄漏
date: 2025-09-21 19:36:26
tags:
    - Node
    - 内存泄漏 
categories:
---
在[Node服务内存泄漏问题排查](https://mp.weixin.qq.com/s/9FtnMtRtWNu2SU_8d4QR4Q)一文中，我们介绍了排查内存泄漏的方法。其实最初我教道友的并不是这个方法，所以道友没有找到内存泄漏原因，后来道友把他的代码发我排查之后，给他找到了解决办法。

后来为了写Node服务内存泄漏问题排查一文，更深入的研究了下这个内存泄漏，才知道主要是看 Retained Size (指的是一个对象被垃圾回收后，能实际释放的内存量)，从上往下找就行，简单易懂。所以还是得多写文章才行啊。

写完Node服务内存泄漏问题排查一文后，用新的方法，一下子就找到了是console内存泄漏了。困惑的是最右边Retained Size对不上，没搞明白。

至于解决的办法也很简单，加上 global.console = undefined 就行了，代码如下

```
app.post("/generateCookies", (req, res) => {
    let url = req.body.url;
    let html = req.body.html;
    let cookies = sdk.generateCookies(url, html);
    global.console = undefined
    res.json({ code: 0,'data': {'cookies': cookies}})
}
```

问题是为啥 console 会引发内存泄漏？看了代码后，可以知道它重定义了 console 里的方法，像log, info这些方法。对于这个问题有两种解决办法，一种是把这些重定义代码删掉，如果重定义代码在控制流或者vmp里，就不好找到重定义代码并删除。

另一种是不让它重定义这些方法。而不让它重定义这些方法，就可以用到Object.freeze 在JavaScript逆向时的妙用一文中介绍的 Object.freeze 方法。把console给冻结了，不让它修改，也就不会有内存泄漏。最终代码如下

```
Object.freeze(console)
app.post("/generateCookies", (req, res) => {
    let url = req.body.url;
    let html = req.body.html;
    let cookies = sdk.generateCookies(url, html);
    res.json({ code: 0,'data': {'cookies': cookies}})
}
```

后来发现，这个禁用console 是JavaScript Obfuscator 里的逻辑，剥离业务代码后，将测试代码放在https://github.com/dengshilong/js_reverse/tree/main/disable_console 这里，有兴趣的话可以去测试下 console 引发的内存泄漏。

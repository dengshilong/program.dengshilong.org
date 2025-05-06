title: 爬虫还是保持userAgent一致来得稳
date: 2025-05-06 19:31:21
tags:
    - 爬虫
    - jsdom
categories:
---
一般反爬在生成加密参数的时候，都会取navigator里的userAgent属性，然后生成加密参数。在使用requests库的时候，爬虫也会设置下headers里的User-Agent值。但很多时候爬虫并没有保持这两个值一致。

在使用补环境生成参数的时候，如果要支持动态传入userAgent，就得在调用参数生成接口的时候增加userAgent参数，并传到补环境代码里设置navigator.userAgent，爬虫偷懒的时候就会省掉这一步，直接固定写死navigator.userAgent。

还有在使用jsdom补环境生成参数的时候，会错误设置userAgent。如果像以下代码一样设置userAgent就是错的

```
const { JSDOM } = require('jsdom');

// 自定义的 userAgent 字符串
const myUserAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3';

// 创建 jsdom 实例并设置 userAgent
const dom = new JSDOM(``, {
  userAgent: myUserAgent
});

console.log(dom.window.navigator.userAgent); // 输出类似Mozilla/5.0 (darwin) AppleWebKit/537.36 (KHTML, like Gecko) jsdom/19.0.0 这种包含jsdom的userAgent
```

jsdom里正确的做法是使用ResourceLoader设置userAgent
```
const jsdom = require("jsdom");  // 引入 jsdom
const { JSDOM } = jsdom;  // 引出 JSDOM 类， 等同于 JSDOM = jsdom.JSDOM
const userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
const resourceLoader = new jsdom.ResourceLoader({
  userAgent: userAgent
});
const dom = new JSDOM(``, {
    url: "https://example.org/",
    referrer: "https://example.com/",
   resources: resourceLoader,
});
window = dom.window
console.log(window.navigator.userAgent) // 输出是Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
```

有一些反爬在不严格的时候即便userAgent不一致也让爬虫通过，但风控严格的时候userAgent不一致又不让爬虫通过，让爬虫摸不着头脑，得排查老半天。所以爬虫为了稳妥起见，还是得保持navigator里的userAgent属性和headers里的User-Agent值一致。

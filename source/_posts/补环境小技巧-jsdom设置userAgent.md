title: 补环境小技巧-jsdom设置userAgent
date: 2024-04-07 10:07:48
tags:
    - jsdom
    - 补环境
    - 反爬
    - 逆向
categories:
---
很多道友使用jsdom来补环境，但没有设置好userAgent(以下简称ua), 如果生成的token中有使用到ua, 反爬人员就可以通过分析token发现是由jsdom生成的，于是针对jsdom的特征做检测。所以使用jsdom时，设置ua很重要。

下面我们来看看怎么设置ua, 网上常见的设置ua代码如下

```
const jsdom = require("jsdom");
const { JSDOM } = jsdom;
const userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
const dom = new JSDOM(``, {
    url: "https://example.org/",
    referrer: "https://example.com/",
    userAgent: userAgent,
});
window = dom.window
console.log(window.navigator.userAgent)
```

输出结果为 Mozilla/5.0 (darwin) AppleWebKit/537.36 (KHTML, like Gecko) jsdom/24.0.0, 有jsdom特征，与设置的ua不一致。

尝试添加如下代码

```
window.navigator.userAgent = userAgent
console.log(window.navigator.userAgent)
```
输出结果依然为 Mozilla/5.0 (darwin) AppleWebKit/537.36 (KHTML, like Gecko) jsdom/24.0.0

继续尝试增加如下代码

```
navigator = {
    userAgent: userAgent
}
console.log(window.navigator.userAgent)
```
输出结果依然为 Mozilla/5.0 (darwin) AppleWebKit/537.36 (KHTML, like Gecko) jsdom/24.0.0

查看官方文档，使用ResourceLoader可以修改ua, 代码如下

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
console.log(window.navigator.userAgent)
```
输出结果为 Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36, 已经没有jsdom的特征，目标达成。

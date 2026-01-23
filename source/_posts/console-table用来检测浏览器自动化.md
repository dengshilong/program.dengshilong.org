title: console.table用来检测浏览器自动化
date: 2026-01-23 18:27:35
tags:
    - 逆向
    - 爬虫
categories:
---
在之前文章[听说你Selenium和Playwright自动化无敌，来试试这两个站点吧](http://program.robinjia.cc/2026/01/15/%E5%90%AC%E8%AF%B4%E4%BD%A0Selenium%E5%92%8CPlaywright%E8%87%AA%E5%8A%A8%E5%8C%96%E6%97%A0%E6%95%8C%EF%BC%8C%E6%9D%A5%E8%AF%95%E8%AF%95%E8%BF%99%E4%B8%A4%E4%B8%AA%E7%AB%99%E7%82%B9%E5%90%A7/)里，我们说过 Selenium 和 Playwright 会被重定向到空白页，于是就研究了下，发现都无法打开开发者工具，这让我想到 disable-devtool，在[解决disable-devtool控制台反调试](http://program.robinjia.cc/2025/09/21/%E8%A7%A3%E5%86%B3disable-devtool%E6%8E%A7%E5%88%B6%E5%8F%B0%E5%8F%8D%E8%B0%83%E8%AF%95/)里我们就有研究过这个库。从浏览器设置里，强制打开开发者工具，在 console 里看到好多日志，确定是 disable-devtool。于是大胆猜测，是因为 disable-devtool 导致浏览器自动化重定向了，即便没有打开开发者工具。

在本地写了个测试页面, 测试代码见https://github.com/dengshilong/js_reverse/blob/main/disable_devtool/test.html，用浏览器自动化去访问，果然会被重定向到空白页面。于是就去排查disable-devtool，总共就几种测试类型，那就一种一种测试下。当测试到 Performance 类型时，发现浏览器自动化会重定向到空白页。看了下代码，找到最终原因 console.table。

在没有打开开发者工具时，浏览器自动化 console.table 输出大对象时也耗时很久，和打开开发者工具时一样，所以就被判定为打开开发者工具，会被重定向。而正常浏览器在没有打开开发者工具时，console.table 输出大对象耗时很短。原因找到了，剩下的就好办了。

我想这就是纯纯的误伤了，disable-devtool 本意是用来检测用户打开开发者工具的，没想到把自动化工具也检测出来了。不过这确实可以作为检测自动化工具的一个因素，一旦发现console.table耗时很长，是自动化爬虫的可能就很高。

那么问题来了，为什么同样是自动化工具，在没有打开开发者工具时，Selenium 和 Playwright 执行 console.table 耗时很长，而 DrissionPage 却耗时很短呢？

title: 用补环境框架测试inCaplusa之reese84
date: 2024-02-24 11:39:50
tags:
    - AST
    - 逆向
    - 爬虫
    - JavaScript
categories:
---
今年如约开启了海外反爬之旅，对常见的四个海外反爬中inCaplusa，Akamai, CloudFlare(一般称为5秒盾), reCaptcha粗略评估后，觉得inCaplusa最为简单，决定先挑软柿子捏，于是先拿inCaplusa试试水。

打开网站，会先返回一段会执行eval的js, 用于生成___utmvc这个cookie, 这段js是个ob混淆，此时祭出蔡老板的ob解混淆工具搞一搞就好了，不难。很多网站没有这个cookie也没关系，可以先不看。

之后是get请求一份网站对应的版本文件，然后会post请求一次版本文件相同的url, 其中返回的token就是reese84。需要说明的是，即便inCaplusa觉得有异常，也会返回这个token, 也就是说token不一定有效，得拿去请求了才知道对不对。一般拿去请求时，状态码不是403就代表reese84是有效的。

拿到版本文件，先进行AST还原，然后开始补环境。不得不说，这个环境校验是真的细，常规的如Canvas, WebGL, font, window["Function"]["prototype"]["toString"]['toString'](), window["Function"]["prototype"]["call"]['toString']()等检测。还有第一次见的类似window["Object"]["getOwnPropertyNames"](Function.prototype.toString)的检测, 这个得能做到只返回['length', 'name']。还有iframe里的contentWindow检测，这里就不一一列举了。

好在代码结构很清晰，可以一步一步调试，补到一半补累了，于是改成扣代码了。花了一天时间扣了下代码能通过之后，信心大增。拿着这个网站的代码去测试其它网站，发现过不去，于是继续补环境，没有全部补完就能过了，估计是校验不严格。测试了几个其它的网站，都能通过，美滋滋了。

目前只是测试了reese84有效性，后续风控之类的还没涉及到。总的来说，如果不是校验不严格，补环境挺不容易的，太多细节了，用来完善补环境框架再好不过了。

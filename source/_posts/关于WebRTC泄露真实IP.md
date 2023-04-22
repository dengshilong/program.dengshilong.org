title: 关于WebRTC泄露真实IP
date: 2023-04-15 20:24:28
tags:
    - WebRTC
    - 逆向
categories:
---
最近技术群里分享了篇文章[《WebRTC泄露源IP的防范措施》](https://mp.weixin.qq.com/s/A5dd7WXojGBzsz52_iLtJQ)，关于WebRTC泄露真实IP，在[我对反爬的一些理解](https://mp.weixin.qq.com/s/vk6e14QaqMEJ6FUKQnUKLg)中其实也提到过这个问题

对于浏览器环境的检测，有Canvas指纹，Webgl指纹，Audio指纹，字体指纹，还有WebRTC指纹等等。WebRTC可以获取到客户端的实际内外网IP，即便浏览器加了代理。对Canvas指纹，Webgl指纹，Audio指纹，字体指纹做校验是为了防止爬虫用程序批量抓取，因为这种批量抓取，指纹大都是一样的。当然对于有经验的爬虫，这些都防不住，指纹可以修改，WebRTC可以禁用。

一些知名厂商的反爬方案中就有用到WebRTC这个漏洞，如果使用浏览器采集的时候，发现并发上不去，很有可能是因为WebRTC暴露了真实IP。

网上说解决的办法是安装WebRTC Leak Shield等类似插件，在测试网站上[https://ip8.com/webrtc-test](https://ip8.com/webrtc-test)可以测试是不是生效，加上代理，安装插件后，测试发现确实生效，没有暴露真实IP。但在[https://api.ipify.org/](https://api.ipify.org/)网站上测试的时候，还是发现暴露了真实IP，目前还不知道为啥。

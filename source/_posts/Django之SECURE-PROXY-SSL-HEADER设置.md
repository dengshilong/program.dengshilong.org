title: Django之SECURE_PROXY_SSL_HEADER设置
date: 2016-11-18 21:00:10
tags:
    - Django
    - HTTPS
categories:
---
因为服务器上HTTP和HTTPS一起存在，所以[分享接口](http://mp.weixin.qq.com/wiki/7/aaa137b55fb2e0456bf8dd9148dd613f.html#.E5.88.86.E4.BA.AB.E6.8E.A5.E5.8F.A3)这里出了一些问题。

在调用分享接口生成签名时，签名用的url必须是调用JS接口页面的完整URL，但因为存在http和https两种，而Django其实不知道客户端到底是访问http还是https，所以产生了问题。如果写死http, 则访问https时，微信分享签名出错；相反的，如果写死https, 则访问https时，微信分享签名会出错。有什么解决的办法？

查看request对象，知道scheme这个属性，于是看到[SECURE_PROXY_SSL_HEADER](https://docs.djangoproject.com/en/1.10/ref/settings/#secure-proxy-ssl-header)设置。

大意就是当在settings里配置了SECURE_PROXY_SSL_HEADER，Django就会到request.META里读取相关参数，如果有设置https，则这是一个https请求。而相关参数需要代理服务器设置，我这里使用Nginx。

于是在Nginx配置里，当访问的是https时，就加上
```
proxy_set_header HTTP_X_FORWARDED_PROTO https;
```
然后在Django的settings配置里加上
```
SECURE_PROXY_SSL_HEADER = ('HTTP_HTTP_X_FORWARDED_PROTO', 'https')
```
这里之所以会多一个HTTP_是因为Django默认会给request.ME如此配置后，request.scheme就会返回http,  当请求是https时，则会返回https。分享的签名正确，问题得到解决。

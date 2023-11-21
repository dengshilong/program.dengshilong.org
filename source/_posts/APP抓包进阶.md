title: APP抓包进阶
date: 2023-11-21 19:57:07
tags:
    - APP
    - 逆向
categories:
---

在[APP抓包入门](http://program.robinjia.cc/2022/07/10/APP%E6%8A%93%E5%8C%85%E5%85%A5%E9%97%A8/)中，我们有说过有一些复杂的APP，抓包软件是抓不到HTTPS包，这其中的原因有很多，比较常见的如SSL Pinning，还有双向认证，还有一些情况是不走HTTP协议。这里我们来解决最常见的SSL Pinning问题。

SSL pinning简单来说就是证书绑定，SSL证书绑定，即客户端内置了服务端真正的公钥证书。在 HTTPS 请求时，服务端发给客户端的公钥证书必须与客户端内置的公钥证书一致，这样请求才会成功。而使用抓包软件后，抓包软件的公钥证书和客户端内置的公钥证书不一致，这样请求就会失败。

网上有很多解决办法，其中如[DroidSSLUnpinning](https://github.com/WooyunDota/DroidSSLUnpinning), [r0capture](https://github.com/r0ysue/r0capture), 这里我们使用DroidSSLUnpinning来解决这个问题。

查看DroidSSLUnpinning的使用方法，进入ObjectionUnpinningPlus目录，使用hooks.js脚本即可。需要安装frida使用。frida脚本使用方法有两种，一种attach, 一种spawn。com.example.mennomorsink.webviewtest2 是应用包名，可使用frida-ps -U命令进行查找报名。也可以使用jadx反编译工具，在资源文件AndroidManifest.xml中的第一行，找到package字段即可。有一些frida版本会提示--no-pause无法使用，去掉这个参数即可。

* 使用方法1 attach : frida -U com.example.mennomorsink.webviewtest2 --no-pause -l hooks.js
* 使用方法2 spawn : frida -U -f com.example.mennomorsink.webviewtest2 -l hooks.js --no-pause


至于r0capture的使用，可以查看r0capture仓库里的使用文档。这个库功能更强，但要配合WireShark使用。


title: 使用Canvas指纹插件被检测到
date: 2024-01-06 16:53:22
tags:
    - 
categories:
---
自从知道了网站会采集浏览器设备指纹和WebRTC泄漏真实IP后，在浏览器上常年挂着指纹对抗插件，Canvas Fingerprint Defender，Font Fingerprint Defender，WebGL Fingerprint Defender，WebRTC Network Limiter。突然某天发现自己访问某地图网站时返回了假数据(假数据的形式是不返回围栏边界数据，地址可能出现错误)，在排查问题后，锁定了Canvas Fingerprint Defender插件和WebGL Fingerprint Defender插件，只要打开这两个插件中的任意一个都会返回假数据。

于是排查Canvas Fingerprint Defender插件，查看这个插件的代码，发现主要是hook了toBlob，toDataURL，getImageData方法。于是尝试自己写了一个hook toDataURL方法，用了V佬的toString保护函数，代码如下

```
(function() {
    //'use strict';
    console.log('start hook')
    var v_saf;
    !function(){var n=Function.toString,t=[],i=[],o=[].indexOf.bind(t),e=[].push.bind(t),r=[].push.bind(i);function u(n,t){return-1==o(n)&&(e(n),r(`function ${t||n.name||""}() { [native code] }`)),n}Object.defineProperty(Function.prototype,"toString",{enumerable:!1,configurable:!0,writable:!0,value:function(){return"function"==typeof this&&i[o(this)]||n.call(this)}}),u(Function.prototype.toString,"toString"),v_saf=u}();

    var v_new_toggle = false;
    var v_console_logger = console.log
    var v_console_log = function(){if (!v_new_toggle){ v_console_logger.apply(this, arguments) }}

    const myToDataURL = HTMLCanvasElement.prototype.toDataURL;
    Object.defineProperties(HTMLCanvasElement.prototype, {
        toDataURL: {
            value: v_saf(function toDataURL(){
                v_console_log("[*] HTMLCanvasElement -> toDataURL[func]", [].slice.call(arguments));
                debugger;
                return myToDataURL.apply(this, arguments)
            })
        },
    })
    // Your code here...
})();
```
把代码放在油猴里跑，神奇的是，即便在toDataURL啥都没有做，toDataURL生成的结果和修改之前一模一样，依然能被检测到。使用Object.getOwnPropertyDescriptor(HTMLCanvasElement.prototype, 'toDataURL')和HTMLCanvasElement.prototype.toDataURL.toString()查看，和未使用hook之前几乎长的一模一样。这就超过了我所学的JavaScript知识了，涉及到知识盲区了。感兴趣的大佬可以试试，解决了的话可以告诉我一声。

一时半会找不到问题所在，于是尝试下载Chromium，照着网上[随机Canvas画布的文章](https://blog.csdn.net/weixin_42557907/article/details/123059379), 自己编译了个Chromium, 在[browserleaks.com](https://browserleaks.com/canvas)上测试了下，Canvas指纹可以随机了，访问网站也没有给假数据。

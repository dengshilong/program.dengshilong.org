title: 解决disable-devtool控制台反调试
date: 2025-09-21 19:19:45
tags:
    - 反调试
    - 逆向
    - disable-devtool
categories:
---
从业以来第一次遇到站点无法使用快捷键打开开发者工具，猜测是监听了键盘事件，于是只好在浏览器设置里点击打开

发现打开开发者工具后，会跳转about:blank空白页面，于是把网页代码下载到本地，之后在代码里搜索about:blank, 发现如下可疑代码

把window.location.href="about:blank"删除之后，用Charles等抓包工具里的Map Local(映射本地文件)进行文件替换。此时还是无法使用快捷键打开开发者工具，但依然通过浏览器设置打开开发者工具，好在页面不再跳转空白页。


此时console日志一直在打印，跳到日志输出的代码文件，大概看了下反调试逻辑，用了很多方案，窗口大小，时间等等。在代码文件里找到一个链接 https://theajack.github.io/disable-devtool/404.html，于是我们知道这个反调试是用的https://github.com/theajack/disable-devtool 这个库。

查看这个库的源码，我们可以知道它是通过监听keydown事件，屏蔽了打开开发者工具的快捷键。代码片段如下

```
target.addEventListener('keydown', (e) => {
  e = e || target.event;
  const keyCode = e.keyCode || e.which;
  if (
    keyCode === KEY.F12 || // 禁用f12
    isOpenDevToolKey(e, keyCode) || // 禁用 ctrl + shift + i
    isViewSourceCodeKey(e, keyCode) // 禁用 ctrl + u 和 ctrl + s 查看和保存源码
  ) {
    return preventEvent(target, e);
  }
}, true);
```

之后看了下初始化代码，找到绕过的办法。只要不让它执行initInterval，disableKeyAndMenu，initDetectors这几个函数即可，直接设置disableDevtool.isRunning = true即可。 网站代码经过混淆，但没有高度混淆，就webpack打包了下，在对应的代码里找到isRunning变量，把它设置为true即可。

```
if (disableDevtool.isRunning) return r('already running');
initIS(); // ! 首先初始化env
initLogs(); // 然后初始化log
mergeConfig(opts);
// 被 token 绕过 或者
if (checkTk()) return r('token passed');
// 开启了保护seo 并且 是seobot
if ((config.seo && IS.seoBot)) return r('seobot');
disableDevtool.isRunning = true;
initInterval(disableDevtool);
disableKeyAndMenu(disableDevtool);
initDetectors();
return r();
```

最后发现disable-devtool这个库挺多star的, 作者是国内开发者，是个精力旺盛的开发，作者还给了一个测试网站

https://theajack.github.io/disable-devtool/，有兴趣的可以试试。

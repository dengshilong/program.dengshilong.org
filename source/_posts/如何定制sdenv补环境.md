title: 如何定制sdenv补环境
date: 2025-09-21 19:13:52
tags:
    - 逆向
    - 某数
    - jsdom
    - JavaScript
    - 补环境
categories:
---
在 [某数反爬方案调研](https://mp.weixin.qq.com/s/QJ9X1O1EV6g22CAAhacaPA) 和 [听闻sdenv被反爬](https://mp.weixin.qq.com/s/vY_Y9AzEJ41K4utt-uKaYg) 里，我们都提到了sdenv, 它就是一个在 jsdom 上魔改的某数补环境方案。而在听闻sdenv被反爬里，也提到过它的很多环境设置还是有问题，那么如果要魔改sdenv又要如何操作呢？有道友问了这个问题，这里记录一下。

sdenv 执行的时候有一行代码很关键，那就是 browser(window, 'chrome') 这行，加上这行它会去加载一个写好的 chrome 环境代码，而这些代码就在browser/chrome目录里。所以我们要定制sdenv, 也可以在这里增加代码。

举个简单例子来说，sdenv 在执行window.document.toString()时返回的结果是[object Document]而不是 [object HTMLDocument]，有什么办法修改它的这个toString吗？其实只要修改browser/chrome目录里的document.js文件就好, 给它加上如下两行代码，之后window.document.toString() 就会发生变化了。

```
window.document.toString = function toString() {
    return '[object HTMLDocument]'
}
sdenv.tools.setFuncNative(window.document.toString)
```

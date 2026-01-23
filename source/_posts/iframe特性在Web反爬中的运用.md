title: iframe特性在Web反爬中的运用
date: 2026-01-23 18:30:01
tags:
    - 爬虫
    - 逆向
categories:
---
最近又发现一个很有意思的特性，和 iframe 相关。

iframe 是在 HTML 页面里用来嵌入其它页面的，它有个 contentWindow 属性，会和当前页面的 window 不一样。写一段测试代码看看就知道了：

```
a = document.createElement('iframe')
document.body.appendChild(a)
console.log(a.contentWindow != window)
console.log(a.contentWindow.console != window.console)
b = document.createElement('iframe')
document.body.appendChild(b)
console.log(a.contentWindow != b.contentWindow)
```

在浏览器里，上面三个判断都输出 true，这就说明 iframe 里的 window 和当前页面的 window 是独立的。

如果[《console.table 用来检测浏览器自动化》](http://program.robinjia.cc/2026/01/23/console-table%E7%94%A8%E6%9D%A5%E6%A3%80%E6%B5%8B%E6%B5%8F%E8%A7%88%E5%99%A8%E8%87%AA%E5%8A%A8%E5%8C%96/)这篇文章里提到的 console.table 是从 iframe 里取的，那么直接修改 console.table 的方法就会失效——因为改的是当前页面里的 console.table，没法直接修改 iframe 里的 console.table。

如果代码是静态的还好处理：等创建好 iframe 后，再修改里面的 console.table。但如果是动态的，那就麻烦了，得再去想办法修改 iframe 里的 console.table。


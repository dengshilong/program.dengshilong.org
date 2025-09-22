title: Node服务内存泄漏问题排查
date: 2025-09-21 19:32:04
tags:
    - Node 
    - 内存泄漏
categories:
---
在使用Express搭建Node服务时，有一个非常值得关注的问题，那就是内存泄漏。内存泄漏会导致服务越来越慢，直至服务崩溃。

最近有个道友反馈，他的服务会内存泄漏，我的服务和他的功能一样，那么也一样会内存泄漏。于是我在Express服务里再加一个接口，用于dump出服务的内存，主要就是使用v8模块的writeHeapSnapshot函数，代码如下。

```
const v8 = require("v8")
app.get("/dump", (req, res) => {
    try {
        const fileName = v8.writeHeapSnapshot();
        console_log(`Heap snapshot written to: ${fileName}`);
        res.status(200).send(`Heap snapshot written);
    } catch (err) {
        res.status(500).send("Internal Server Error");
    }
});
```

接下来就是请求服务接口，等它内存泄漏之后，调用这个dump内存接口，生成如Heap.20250710.170608.4721.0.001.heapsnapshot 这种文件。之后打开Chrome 开发者调试工具，在Memory里, 导入内存镜像，开始分析内存泄漏原因。

我们可以看到Retained Size(指的是一个对象被垃圾回收后，能实际释放的内存量) 几乎都在global里, 于是重点排查这里。

点开global这里，我们能看到，Retained Size都集中在fetch这个变量，于是我们在代码的最后添加global.fetch = undefined 来释放内存，最终代码如下。之后重启服务，继续测试，内存泄漏问题不再出现， 收工。

```
function executeJs(code, cookies, initParam) {
    // 拼接新的 JS 代码
    const newHeadJs = headJs + ";;;\n" + "window.param=" + JSON.stringify(initParam) + ";;;;\n" + code;
    // 执行拼接的 JS 代码
    eval(newHeadJs);
    // 构造返回结果
    const result = {
        cookies: utils.changeToCookies(window.document.cookie)
    };
    // 清除全局 fetch
    global.fetch = undefined;
    return result;
}
```

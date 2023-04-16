title: vm2也是可以被检测
date: 2023-04-16 20:19:16
tags:
    - vm2
    - 补环境
    - selenium
    - 逆向
categories:
---
之前因为Node环境容易被检测，就用vm2沙盒来跑，可以避免很多检测。虽然大佬们都说vm2也是可以被检测的，但一直能跑，就一直用着。

最近在搞一个网站，一直过不去，仔细调试后发现是因为VM2_INTERNAL_STATE_DO_NOT_USE_OR_PROGRAM_WILL_FAIL.handleException这个东西。搜索vm2的源码，在transform.js里可以找到如下代码

```
const name = assertType(param, 'Identifier').name;
const cBody = assertType(node.body, 'BlockStatement');
if (cBody.body.length > 0) {
    insertions.push({
        __proto__: null,
        pos: cBody.body[0].start,
        order: TO_LEFT,
        coder: () => `${name}=${INTERNAL_STATE_NAME}.handleException(${name});`
    });
}
```
类似的代码还有好几次，作为实用主义，就不细细研究vm2为啥要加上这些代码，简单粗暴的把这一部分删掉后就跑起来了。

之前用jsdom, jsdom被检测，现在用vm2, vm2也被检测，对抗之路真是永无止境。看来还是得selenium一把梭才是王道啊，只是selenium如何方便的做成一个服务，工程化问题如何解决呢，这是个问题，要不然selenium自动化真是香喷喷。

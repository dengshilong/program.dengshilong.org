title: wasm补环境初体验
date: 2023-06-23 15:41:21
tags:
    - 补环境
    - 逆向
    - wasm
    - WebAssembly
categories:
---
wasm补环境初体验

最近看到群里在讨论，y小白也写了篇相关的[文章](https://mp.weixin.qq.com/s/8W6tRC-gA0FG2OD5o-RmOg)，于是也想试试。wasm 即 WebAssembly，这还是第一次遇到了。

放在补环境框架里跑一跑，就遇到 vm2 读取 wasm 文件的问题。具体是这样的，在 Node里先把文件加载进来后，在传到 vm2 沙盒里时，一般都是通过 sandbox 对象传入。代码如下

```
wasmCode = fs.readFileSync('test.wasm');
const sandbox = {
    wasmCode: Buffer.from(wasmCode).buffer,
}

const vm = new VM({
    sandbox: sandbox,
});
```

然后 sandbox 会被 proxy 代理了，此时发现无法使用 WebAssembly.instantiate 来实例化 WebAssembly 代码。查看 vm2 源码就会发现代码里会对sandbox进行操作。目前只想到通过修改 vm2 源码的办法来解决这个问题。这到时候发布啥的就会麻烦一些，需要单独打Docker镜像。

解决这个问题后就简单多了，缺啥补啥就行了，补出来的token直接就能访问。估计现在还是初级版本，还在持续更新中，目前没有什么特别的检测点。

为了便于发布，顺便搞了个Node的版本，有了之前的 vm2 版本基础，补起来就挺顺畅的，没遇到什么困难。

唯一值得一提的是，它这个环境会根据传入的参数不同，做不同的环境检测，走不同的检测分支，这还是第一次见这种情况。整体下来并没遇到什么难点，估计后面会越来越难了，得先准备起来。

title: Node服务设置--max-old-space-size参数
date: 2024-07-16 20:51:35
tags:
    - Node
    - PM2
categories:
---
Node服务设置--max-old-space-size参数

可以先问问GPT这个参数是做什么的

--max-old-space-size 是 Node.js 运行时的一个参数，它用来设置 V8 引擎的老生代内存限制。
V8 的内存空间主要分为新生代空间（Young Generation）和老生代空间（Old Generation），这两种空间的大小决定了应用程序可以使用的最大内存。新生代空间通常较小，并且垃圾回收频率较高；而老生代空间较大，并且垃圾回收频率较低。
当你设置了 --max-old-space-size 的值，你就在 V8 引擎运行时告诉它，它在老生代空间可以使用的最大内存量。如果你的应用程序尝试超过这个限制，V8 引擎会抛出一个 FATAL ERROR: Reached heap limit Allocation failed 的错误，表示内存已用尽，无法分配新的内存。
请注意，--max-old-space-size 只是 V8 引擎可以使用的总内存的一个部分，还有其他部分是由 V8 内部使用的，例如它的执行代码和堆栈空间等。所以，如果你的系统内存较少，你可能会需要减小 --max-old-space-size 的值，以确保其他重要的系统进程也能正常运行。

在PM2中我们就可以如此启动服务 pm2 start server.js -i 2 --node-args="--max-old-space-size=800" --no-daemon

--max-old-space-size 这个参数比 --max-memory-restart 好用多了，它会尝试进行内存回收，能回收了，就不重启进程，不能回收就才会重启进程，这样可以减少 502 服务器错误。

有了这个参数，也不需要再使用强制内存回收插件了，因为本身自带内存回收。唯一的问题是，PM2守护的进程内存都是从0开始，然后进程一起到达设置的老生代内存大小，此时CPU占比会很高，可能会影响服务执行。

title: Node服务高并发之PM2使用
date: 2023-07-02 17:23:17
tags:
    - PM2
    - Node
    - JavaScript
    - 并发
categories:
---
和道友交流的时候，发现他对Node服务高并发一知半解，于是和他讲了下自己的理解，他说受益匪浅，于是写文章记录下来，希望能帮助到其他人。

当我们用 Express 搭建好一个 token 生成服务给其他开发调用时，我们就要开始考虑服务的性能，考虑服务的并发能力。同时也要考虑服务如何方便部署，方便更新程序。而由于 token 生成服务都是 CPU 密集型程序，所以只能通过提高进程数，提高 CPU 核数来提高并发能力。

刚来公司的时候，看到接手的 token 生成服务是这样部署的，在连续的几个端口中，比如5000，5001，5002，每个端口用 Node 启动一个 Express 服务，客户端调用的时候，随机取其中一个端口访问。服务需要更新的时候，得一个一个 Node 进程杀死后再重新启动，过程很不友好。

正好之前做过一点前端开发，前后端分离时用到过 PM2 来管理Node进程, 于是将这些服务都用 PM2 来管理，并在全组范围内推广使用 PM2，现在我们所有的 token 生成服务都用 PM2 来管理，就挺好。

PM2 很好用的一点是可以设置进程超过一定内存后就重启，通过配置 --max-memory-restart 参数即可实现。这个功能就很实用，因为 JavaScript 的闭包使用真的很容易内存泄漏，想找到原因不容易。为了不影响服务器上的其它进程，得不断重启Node进程。

单台机器上，CPU核数和进程数一致，此时并发性能最高。如果这样了还不能满足业务需求，只能堆机器，在多台机器上部署。

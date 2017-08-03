title: Tornado开启多进程
date: 2017-08-03 20:49:39
tags:
    - Tornado
categories:
---
之前服务是用 Tornado 启动，但响应速度很慢，有时候会被一些任务给卡死，于是一直想提高性能，后来发现是没有使用多进程。看到 [tornado.httpserver — Non-blocking HTTP server](http://www.tornadoweb.org/en/stable/httpserver.html) 中的配置，于是加上多进程。

```
sockets = tornado.netutil.bind_sockets(8888)
tornado.process.fork_processes(4)
server = HTTPServer(app, xheaders=True)
server.add_sockets(sockets)
IOLoop.current().start()
```
但是在 debug 模式下，上面的配置是会报错的，所以 debug 模式下还是使用单进程配置。

```
server = HTTPServer(app)
server.listen(8888, xheaders=True)
IOLoop.current().start()
```
现在响应速度有了质的飞跃。

至于 xheaders 配置，是为了获取用户的真实 IP。

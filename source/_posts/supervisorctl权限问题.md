title: Supervisor之supervisorctl权限问题
date: 2016-12-25 21:47:04
tags:
    - Supervisor
categories:
---
执行`supervisorctl status`会提示如下错误
```
error: <class 'socket.error'>, [Errno 13] Permission denied: file: /usr/local/lib/python2.7/socket.py line: 228
```

在[Permession denied error when use supervisorctl #173](https://github.com/Supervisor/supervisor/issues/173)里找到如下解决办法
```
[unix_http_server]
file=/tmp/supervisor.sock   ; (the path to the socket file)
chmod=0766                 ; socket file mode (default 0700)
```
就是修改sock的权限

title: Shell命令之kill
date: 2016-08-07 12:15:24
tags:
    - Shell
    - kill
categories:
    - shell
---
kill命令主要用来杀进程，以前不懂，一只都用`kill -9`, 现在才发现打错特错。

最近在学习使用Supervisor管理进程，测试Supervisor被杀死之后的情况。发现用`kill -9`杀死Supervisor后，管理的进程会变成孤儿进程。于是请教[the5fire](https://www.the5fire.com/), 他提供了一篇[no use kill 9](http://www.vaikan.com/no-no-no-dont-use-kill-9/), 顿时解决了疑惑。

在Mac上 man kill看到如下说明

```
1       HUP (hang up)
2       INT (interrupt)
3       QUIT (quit)
6       ABRT (abort)
9       KILL (non-catchable, non-ignorable kill)
14      ALRM (alarm clock)
15      TERM (software termination signal)
```

`kill -9`的主要弊端是被杀的进程来不及善后处理就已经死了，这回留下很多问题。所以强烈建议不要使用`kill -9`来杀死进程, 而是使用`kill -15`。

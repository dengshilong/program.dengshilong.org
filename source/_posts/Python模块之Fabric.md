title: Python模块之Fabric
date: 2016-11-26 11:56:33
tags:
    - Python
    - Fabric
categories:
---
[Fabric](http://www.fabfile.org/)用于发布和执行一些系统管理任务，非常方便。

目前[学习笔记](用于发布的脚本如下，很方便。
```

from fabric.api import *
env.hosts = ['43.242.128.158']
env.user = 'dengsl'
def deploy():
    code_dir = '/home/dengsl/program/nodejs/blog'
    with cd(code_dir):
        run("git pull")
         #deploy static site
        run("hexo clean")
        run("hexo g")
        run("cp -r public/* /home/dengsl/program/html/blog/note")
```

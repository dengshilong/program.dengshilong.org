title: PyCharm安装vim插件
date: 2016-04-15 10:17:04
tags: 
    - PyCharm
    -  vim
categories:
    - Python
---
google "pycharm vim", 第一条指向[https://confluence.jetbrains.com/display/PYH/Configuring+PyCharm+to+work+as+a+Vim+editor](https://confluence.jetbrains.com/display/PYH/Configuring+PyCharm+to+work+as+a+Vim+editor)这里，但没有找到我想要的，于是自己在PyCharm里找，终于找到了，记下来。

PyCharm->Preference->Plugins->Install JetBrains plugin, 之后搜索vim找到ideavim, 安装后重启，进入PyCharm已经可以和vim一样编辑代码。

但是连行号都没有，于是想到要给ideavim加个配置文件，可是要加到哪里？打开[http://blog.csdn.net/u010211892/article/details/43274699](http://blog.csdn.net/u010211892/article/details/43274699)看到
```
cp ~/.vimrc ~/.ideavimrc 
```
对啊，vim是.vimrc, ideavim就是.ideavimrc, 没想到啊。

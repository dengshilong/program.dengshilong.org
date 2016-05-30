title: find查找目录下的所有shell脚本
tags:
  - find
  - shell
id: 750
categories:
  - shell
date: 2014-05-27 13:47:28
---

使用命令find . -name *.sh查找当前目录下的所有shell脚本，提示find: 路径必须在表达式之前

之后改成find . -name "*.sh",可行。find结合sed就可以将需要的文件进行替换。

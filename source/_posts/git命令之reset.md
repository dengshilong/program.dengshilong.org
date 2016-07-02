title: git命令之reset
date: 2016-07-02 17:24:38
tags: 
    - git 
    - reset
categories:
    - 编程
---
reset命令用于重置到某个状态。

常用的命令如下
* git reset 
将所有add到缓存区的操作撤销，如果需要对某个文件撤销，可以使用git reset 文件名

* git reset --hard 
撤销所有的修改，可以在--hard后添加版本后，表示reset到某个版本

参考资料:
* [git reset](https://git-scm.com/docs/git-reset)

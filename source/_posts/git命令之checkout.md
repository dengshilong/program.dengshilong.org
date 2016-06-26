title: git命令之checkout
date: 2016-06-26 17:40:20
tags:
    - git
    - checkout
categories:
    - 编程
---
在使用git时，checkout也是一个常用的命令。

* git checkout foo 切换到foo分支
* git checkout foo 当本地没有foo分支时，相当于同步远程分支，此时相当于执行`git checkout -b <branch> --track <remote>/<branch>`
* git checkout -b foo 创建foo分支，其实想到与执行了`git branch foo`和`git checkout foo`两条命令
* git checkout -- file 恢复file文件

## 常见问题
* 在github上看到有远程分支，但git checkout feature_name无法切换到这个分支，此时可能的一个原因是没有拉取远程分支, 此时需要使用`git fetch origin feature-name`进行拉取。

参考资料:
* [git checkout](https://git-scm.com/docs/git-checkout)

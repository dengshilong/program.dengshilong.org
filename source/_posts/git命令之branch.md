title: git命令之branch
date: 2016-06-26 15:59:13
tags:
    - git
    - branch
categories:
    - 编程
---
在开发新功能时，需要创建分支，此时branch命令派上用场了。branch的一些常用命令如下

* git branch foo 创建foo分支

* git branch -d foo 删除foo分支
* git branch 查看本地分支
* git branch -r 查看远程分支

当只是想拉取远程分支时，则需要添加参数, `git branch foo --track origin/foo` 同步远程foo分支。但是，拉取远程分支有更常用的命令`git checkout foo`

## 常见问题
* 在开发的过程中会遇到的问题是，明明github的仓库上有某个分支，使用`git branch -r`却看不到这个分支，这是因为还没有拉取这个分支到本地，此时使用`git fetch origin feature_name`拉取分支后，再次执行`git branch -r`即可看到分支

参考资料:
* [git branch](https://git-scm.com/docs/git-branch)

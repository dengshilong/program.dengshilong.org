title: git命令之fetch
date: 2016-06-26 11:22:40
tags: 
    - git 
    - merge
categories:
    - 编程
---
在使用git的过程中经常遇到这个问题。明明使用`git status`看到`Your branch is up-to-date with 'origin/dev'.` , 但添加自己的修改，提交之后，发现远程分支已经有了修改。这是为何？现在终于明白这个原因。


这里设计到三个概念，本地的dev, 本地的origin/dev, 远程的dev。上面提示中的origin/dev指的是本地的origin/dev，而不是远程的dev. 虽然本地的dev is up-to-date with本地的origin/dev但，origin/dev并没有与远程的dev同步。所以当我们向远程dev push时，才会提示有冲突。

要想让本地的origin/dev与远程的dev同步，可以执行 `git fetch origin dev`, 发现有了更新

```
 * branch            dev        -> FETCH_HEAD
   078c7d1..d71d504  dev        -> origin/dev
```

此时再次执行`git status`, 就会提示已经落后了， `Your branch is behind 'origin/dev' by 8 commits, and can be fast-forwarded.` 

之后使用merge命令将本地的origin/dev合并到本地的dev中`git merge --no-ff origin/dev`

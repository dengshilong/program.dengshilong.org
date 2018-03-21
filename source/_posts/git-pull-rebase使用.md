title: git pull --rebase使用
date: 2018-03-21 20:43:33
tags:
    - Git
categories:
---
最近公司开始使用Gerrit做code review工具，于是才知道git pull还有rebase这个参数。

当本地分支commit后，然后git pull拉取远程分支的提交，之后使用git review生成一个review时，会提示有多个提交。于是想到git rebase, 但是没想到的是git pull也有rebase参数。

在[洁癖者用 Git：pull --rebase 和 merge --no-ff](http://hungyuhei.github.io/2012/08/07/better-git-commit-graph-using-pull---rebase-and-merge---no-ff.html)里提到了pull --rebase的妙用，解决了多年的困惑。之前使用git pull时，老是生成很多无效的merge, 没想到使用git pull --rebase可以解决这个问题

title: git命令之merge
date: 2016-06-26 16:29:15
tags:
    - git
    - merge
categories:
    - 编程
---
分支操作是一个常见的操作。当在某一分支开发完新功能后，需要合并到master分支，此时就需要使用merge命令。

merge有两种方式，一种是fast-forward, 一种是非fast-forward方式。

* git merge feature 使用fast-forward方式合并feature分支
* git merge --no-ff feature 使用非fast-forward方式合并。

这两种方式的差别在于是否保留分支合并的信息。为此特意在github上见了一个[test-git](https://github.com/dengshilong/test-git)仓库。

使用`git log --graph`在master分支上查看log时，可以很方便的看出两种方式的区别。这里添加了一些参数，使结果更简洁
｀git log --graph --pretty=oneline --abbrev-commit｀

```
*   6ce6fab Merge branch 'feature-noff-merge'
|\
| * 710e832 add noff-merge.md
|/
* 5747a77 add merge.md
* d2adf39 Initial commit
```

* 图中merge.md是在feature-merge分支中添加的，使用fast-forward方式merge
* noff-merge.md是在feature-noff-merge中添加的，使用非fast-forward方式merge

参考资料:
* [git merge](https://git-scm.com/docs/git-merge)

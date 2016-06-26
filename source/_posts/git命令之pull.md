title: git命令之pull
date: 2016-06-26 17:20:58
tags:
    - git
    - pull
categories:
    - 编程
---
理解了[fetch](http://program.dengshilong.org/2016/06/26/git%E5%91%BD%E4%BB%A4%E4%B9%8Bfetch/)和[merge](http://program.dengshilong.org/2016/06/26/git%E5%91%BD%E4%BB%A4%E4%B9%8Bmerge/)后，之后再来看git pull就容易多了。在git的官方文档上，有`git pull is shorthand for git fetch followed by git merge FETCH_HEAD`，也就是说git pull是git fetch和git merge的结合，只是这里的merge是fast-forward方式。

依然在[test-git](https://github.com/dengshilong/test-git)仓库上进行测试，

使用｀git log --graph --pretty=oneline --abbrev-commit｀查看log,

```
*   dee871e Merge remote-tracking branch 'origin/master'
|\
| * d28cd1d add no-fast-forward in test-pull.md
|/
* 35bbd63 add fast-forward in test-pull.md
*   6ce6fab Merge branch 'feature-noff-merge'
|\
| * 710e832 add noff-merge.md
|/
* 5747a77 add merge.md
* d2adf39 Initial commit
```

* 在结果中， add fast-forward in test-pull.md使用`git pull`直接拉取远程分支的变化得到的
* 而add no-fast-forward in test-pull.md是通过执行 `git fetch origin master`和`git merge --no-ff origin/master`两个命令后的结果。

从上面的结果可以看出，使用`git fetch`和`git merge --no-ff`更能保存仓库版本变化的轨迹，推荐使用这种方式。

参考资料:
* [git pull](https://git-scm.com/docs/git-pull)

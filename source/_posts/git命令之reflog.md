title: git命令之reflog
date: 2016-07-02 17:55:10
tags:
    - git
    - reflog
categories:
    - 编程
---
当使用git reset回退到某个后，想再回到当前版本，而git log中看不到当前的版本，此时reflog就派上用场了。

* git reflog 查看版本操作信息，在这里可以看到版本号，之后使用git reset进行版本切换

参考资料:
* [git reflog](https://git-scm.com/docs/git-reflog)

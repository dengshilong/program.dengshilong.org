title: git命令之blame
date: 2016-06-26 11:48:45
tags: 
    - git
    - blame
categories:
    - 编程
---
有些时侯我们想知道一个文件的某一行在哪一个版本里被谁修改的，此时git blame就派上用场了。

官方文档里描述如下
```
git-blame - Show what revision and author last modified each line of a file
```

* git blame foo 查看foo文件的修改记录
* git blame -L 20, 30 foo 查看foo文件从20行到30行的修改记录
* git blame -L 20, +30 foo 查看foo文件20行开始的30行修改记录


参考资料:
* [git blame](https://git-scm.com/docs/git-blame)

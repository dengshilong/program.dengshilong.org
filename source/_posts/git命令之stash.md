title: git命令之stash
date: 2016-06-24 20:00:38
tags: 
    - git
    - stash
categories:
    - 编程
---
当你在一个分支中进行修改时，想切换到另外一个分支，但你目前的修改还不能commit, 因为是不完整的，此时stash命令就可以派上用场。

使用git stash操作将目前的操作保持起来，然后切换到另外一个分支，干活完成后再切回来。此时使用git stash apply将之前的操作恢复。


此外还有一些stash操作如
* git stash list 列出所有储藏
* git stash drop 丢弃储藏
* git stash pop 应用并丢弃储藏

有一个需要注意的是，在一个分支中stash起来的修改，也可以应用于其它分支。所以git stash apply时一定要注意分支是否匹配。

其实这也隐藏了stash的一个功能。当你在一个分支上进行修改时，发现你想修改的是另外一个分支，此时你不想reset掉修改。stash派上用场了，先git stash将修改保存起来，然后切换到另外一个分支，之后git stash apply, 这样修改就应用与另外一个分支了。

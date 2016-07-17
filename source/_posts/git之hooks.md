title: git之hooks
date: 2016-07-17 16:34:24
tags:
    - git
    - hooks
categories:
    - 编程
---
如果需要对提交的代码进行检查，可以使用hooks, 也就是钩子，如果需要在代码提交到参考后进行发布，也可以使用hooks.

在初始化git仓库时，在.git目录的hooks目录里提供了一些例子。

在我的学习笔记的仓库里，我定义了post-receive这个hooks, 当deploy出现在commit的说明信息中，就更新学习笔记。

```
#file info
 GIT_REPO=/home/dengsl/program/nodejs/blog
 DEPLOY_DIR=/home/dengsl/program/html/blog/note

 # Get the latest commit subject
 SUBJECT=$(git log -1 --pretty=format:"%s")

 cd $GIT_REPO
 env -i git reset --hard

 #update or deploy
 IF_DEPLOY=$( echo $SUBJECT | grep 'deploy')
 if [ -z "$IF_DEPLOY" ]; then
     echo >&2 "Success. Repo update only"
     exit 0;
 fi

 # Check the deploy dir whether it exists
 if [ ! -d $DEPLOY_DIR ] ; then
 echo >&2 "fatal: post-receive: DEPLOY_DIR_NOT_EXIST: \"$DEPLOY_DIR\""
 exit 1
 fi
 
  #deploy static site
 hexo g
 cp -r public/* $DEPLOY_DIR
```

参考资料:
* [git hooks](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)

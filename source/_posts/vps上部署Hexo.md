title: vps上部署Hexo
date: 2015-12-11 20:38:09
tags: Hexo
categories: 软件安装
---
Hexo一般都是部署到github上去，只是我有vps，干吗不用。

对于部署到vps上，本来是想使用Hexo server，然后用Nginx做反向代理。后来想想，这样耗费资源，于是在网上找到[在VPS上部署hexo](http://blog.berry10086.com/Tech/deploy-hexo-to-vps/)，直接将生成的页面给Nginx服务器，既节省资源，访问速度又更快。只是我还是想通过git管理Hexo代码，就像以前写[MV小站](http://lemonbean.info/)那样。可是对于git不熟悉，上次也没有做笔记。于是在网上找到[VPS上(debian8 jessie)部署hexo(Nginx代理+git部署)](http://blog.15-cm.com/2015/06/05/deploy-hexo-on-vps/)，正是我想要的。具体可以参考这篇，这里只记录遇到的问题。

## 设置ssh密钥登陆vps失败
用ssh-keygen生成密钥之后，将公钥id_rsa.pub的内容复制到vps上的authorized_keys里，一直无法登陆。最后在[linux ssh 使用深度解析（key登录详解）](http://blog.lizhigang.net/archives/249)中找到了解答，原来是authorized_keys文件权限的缘故，这个文件必须设置为600，ssh key登陆才会通过。查看日志文件/var/log/secure可以得道一些帮助。

## git push时无法通过
在master上执行git config receive.denyCurrentBranch ignore即可。

## Hexo生成的css文件没有更新
不知道什么情况，有时候有更新，有时候又没有更新。所以干脆先执行hexo clean后再执行hexo g。另外，git hooks很实用。

在git仓库里添加hooks
```
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
 hexo clean
 hexo g
 cp -r public/* $DEPLOY_DIR
```

现在就可以通过git来发布页面，很有意思。

 

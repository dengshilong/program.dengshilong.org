title: Mac磁盘空间清理之使用OmniDiskSweeper
date: 2019-07-04 21:34:56
tags:
    - Mac
categories:
---
Mac的磁盘空间真的是令人抓狂。每次不知道咋回事，就报磁盘空间将要爆满，我就赶紧去删掉一些没用的文件, 或者执行下[clean_my_mac.sh](https://github.com/mengfeng/clean-my-mac/blob/master/clean_my_mac.sh), 过不了几天，又爆满。

今天已经想不到要删哪个没用的文件，使用du -sh *又太慢，于是只好上网找解决办法。上网查了之后，找到了[OmniDiskSweeper](https://www.omnigroup.com/more)这个清理磁盘空间，竟然很好用。 清理后，空间如下。

```
➜  ~ df -h
Filesystem      Size   Used  Avail Capacity  iused    ifree %iused  Mounted on
/dev/disk1     233Gi  143Gi   90Gi    62% 37424607 23556639   61%   /
```

需要注意的是，使用OmniDiskSweeper时，回到上层目录是用方向键中的向左方向键。

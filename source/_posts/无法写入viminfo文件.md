title: 无法写入viminfo文件
date: 2016-08-27 10:53:44
tags:
    - Linux
    - mount
categories:
    - 软件安装
---
今天服务器上出现了无法写入viminfo文件 /root/.viminfo错误，网上有人说删除~/.viminf*.tmp即可，查看目录没有这些文件。

后来发现是文件都变成了只读，想到上午的时候ext3文件系统出了问题。在网上找到[http://www.ha97.com/5428.html], 执行`df -lhT`，知道是ext4文件系统
想执行`fsck.ext4 -y /dev/vda1`，但不允许。因为这是线上系统。

于是继续找，发现`mount -o remount rw /`, 当时提示`mount: you must specify the filesystem type`, 于是加上文件系统类型，执行`mount -t ext4 -o remount rw /`，之后提示
`mount: cannot remount block device rw read-write, is write-protected`
查看鸟哥的私房菜，使用鸟哥的命令
`mount -o remount,rw,auto/`, 没有反应。

于是求助UCloud的工作人员，他们建议重启服务器。等到晚上，重启服务器，系统就起不来了。于是只好找UCloud的工作人员。后来他们进入单用户模式，修复文件系统，重新mount之后，终于弄好了。

可是线上服务停机了一个多小时，因为是单点服务。看来得再加一台机器了。


参考资料
* https://www.peterdavehello.org/2015/03/error-read-only-file-system/
* http://www.ha97.com/5428.html

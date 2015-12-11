title: Linux挂载U盘
tags:
  - Linux
  - U盘
id: 836
categories:
  - shell
date: 2014-07-17 10:54:14
---

挂载U盘
mount -t auto /dev/sdb1 /mnt/usb
如果在mnt目录下不存在usb目录 则先执行 mkdir /mnt/usb,其中/mnt/usb为挂载目录,也可以使用将U盘挂载到其它目录

之后卸载U盘
umount /mnt/usb

如果是文件名中包含中文，还会遇到乱码问题，所以还要加上-o iocharset=utf8
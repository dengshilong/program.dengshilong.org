title: sed替换文件内容
tags:
  - find
  - sed
  - 子目录
id: 752
categories:
  - shell
date: 2014-05-27 13:55:14
---

使用sed -i 's/text/test/' *.sh将当前目录下(不包括子目录)，所有shell脚本的text替换为test, 其中-i参数是指示需要进行文件内替换，也就是改变文件的内容。

如果需要将子目录的也替换，则可以与find命令结合使用,使用sed -i 's/text/test/' `find . -name "*.sh"` 将当前目录下(包括子目录)，所有shell脚本的text替换为test,
title: 在命令行打开html文件
date: 2018-08-09 19:51:45
tags:
    - Mac
categories:
---
有时候在命令行看到一个html文件，就想在浏览器中打开看看是什么。

此时要么在Finder里找到文件打开，或者在浏览器中用file:// + 文件绝对路径。但总觉得不够好。

今天上午搜索之后，发现[Mac下有open命令](https://www.cnblogs.com/willbin/archive/2013/03/19/2968775.html)

于是可以用open -a safari 文件名， 或者也可以用open -a Google\ Chrome 文件名打开

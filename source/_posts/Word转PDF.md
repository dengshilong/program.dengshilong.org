title: Word转PDF
date: 2016-11-12 23:15:23
tags:
    - Word
    - PDF
categories:
---
最近需要将Word文档转为PDF，正好在阿里云的同学做过，于是请教他，他给了一些参考资料，解决了转换的问题。

其中Jacob因为只能用于Windows平台，所以没有尝试。尝试了JODConverter之后，可以转换，效果还不错，暂定使用它。

只是还是存在一点乱码问题，之后再看看怎么解决。

代码博主已经开源，我把它放在了[Github](https://github.com/dengshilong/DocConverter)上，加上命令行输入，可以见[这里](https://github.com/dengshilong/DocConverter/blob/master/src/com/converter/pdfConverter/OpenOfficePDFConverter.java)，主要使用Apache的common-cli这个库。

之后是在Intellij IDEA导出jar包，参考
[Idea 导出 jar包](https://my.oschina.net/scipio/blog/287634)即可。主要步骤如下
```
（1）File→Project Structure...→Artifacts→+→jar→From modules with .... → 选择一个要执行的main方法

（2）extract to jar

（3）选择manifest的位置：d:\idea\myproject\src

（4）勾选build on make

（5）build -- make project， （如不行，在此之前，执行下mvn clean）

（6）D:\idea\myproject\out\artifacts\ 寻找jar
```

参考资料
* [DOC文档转PDF](http://www.iteye.com/topic/1005741)
* [仿百度文库解决方案（四）——利用JODConverter调用OpenOffice.org服务转换文档为PDF](http://www.cnblogs.com/luckyxiaoxuan/archive/2012/06/14/2549012.html)

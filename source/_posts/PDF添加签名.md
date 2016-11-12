title: PDF添加签名
date: 2016-11-12 23:18:07
tags:
    - PDF
    - 签名
categories:
---
在PDF中需要添加签名信息，在网上找到
[JSignPdf](http://jsignpdf.sourceforge.net/), 虽然两年多没更新了，但至少还能工作。

查看文档，发现美中不足的一点是只能一页一页的签名。

需要注意的一点是，图片必须是透明的，要不能签到PDF上会覆盖文字。


尝试之后，一个可行的签名如下
```
java -jar JSignPdf.jar -kp 111111 -ksf temp.pfx -llx 100 -lly 100 -urx 200 -ury 200 --bg-path Wechat2.png --l2-text '' -V 007_overview.pdf
```
参数的具体意义可以看文档。

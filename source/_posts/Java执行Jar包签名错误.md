title: Java执行Jar包签名错误
date: 2016-12-18 16:59:46
tags:
    - Java
    - Jar
categories:
---
在启动Jar包时，报Exception in thread "main" java.lang.SecurityException: Invalid signature file digest for Manifest main attributes错误。

在[stackoverflow](http://stackoverflow.com/questions/999489/invalid-signature-file-when-attempting-to-run-a-jar)上找到如下方法，解决问题。
```
zip -d you.jar 'META-INF/*.SF' 'META-INF/*.DSA' 'META-INF/*.RSA'
```

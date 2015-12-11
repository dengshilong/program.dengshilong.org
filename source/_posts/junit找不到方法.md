title: junit找不到方法
tags:
  - junit
id: 977
categories:
  - Java
date: 2014-12-13 11:39:20
---

最近迷上了单元测试，在写单元测试时，提示一下错误：
java.lang.NoSuchMethodError: junit.framework.ComparisonFailure.getExpected()Ljava/lang/String;

莫名其妙的，assertFalse怎么可能没有。后来才知道，原来是版本冲突了，因为添加了好多个junit的jar本，而Eclipse只找到最低版本的，将一些低版本的jar去掉就好了。

添加jar这个问题真是蛋疼，在Eclipse里对引用的jar一个目录一个目录的添加，还要肉眼去把低版本的删除，真是麻烦。
title: Wordpress迁移Hexo文件名问题
date: 2016-07-22 21:06:48
tags:
    - Wordpress
    - Hexo
categories:
    - 软件安装
---
在[Wordpress迁移到Hexo遇到的问题](http://program.dengshilong.org/2015/12/11/Wordpress%E8%BF%81%E7%A7%BB%E5%88%B0Hexo%E9%81%87%E5%88%B0%E7%9A%84%E9%97%AE%E9%A2%98/)中说过Wordpress迁移到Hexo时会遇到文件名问题，当时写了个Python脚本解决，现在有了更好的解决办法，于是记下。

在迁移的时候会生成
```
e8-af-ad-e8-a8-80-e7-89-b9-e6-80-a7-e8-bf-98-e6-98-af-e6-9c-89-e5-bf-85-e8-a6-81-e5-ad-a6-e4-b9-a0-e7-9a-84.md
e8-bd-af-e8-bf-9e-e6-8e-a5-e5-92-8c-e7-a1-ac-e8-bf-9e-e6-8e-a5.md
e8-bf-bd-e8-b8-aaquery-too-complex-not-enough-stack-e9-94-99-e8-af-af.md
```
这样的文件名, 原因是文件名是从URL转化而来。后来发现将URL进行encode之后就没有这个问题。在fork出的[hexo-migrator-wordpress](https://github.com/dengshilong/hexo-migrator-wordpress)里解决了这个问题，在github上提交了一个[pull request](https://github.com/hexojs/hexo-migrator-wordpress/pull/16), 但一直没有被合并，匪夷所思。

不过还是可以直接安装我的仓库里的代码来解决这个问题。`npm install https://github.com/dengshilong/hexo-migrator-wordpress.git --save`

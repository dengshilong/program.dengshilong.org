title: CentOS6.5升级git
date: 2016-08-01 20:12:15
tags:
    - git
    - CentOS
categories:
    - 软件安装
---
两年前安装的CentOS6.5, git版本号是1.7.1, 需要升级。

参考[CentOS 6.x 升级 Git](https://segmentfault.com/a/1190000002729908)，安装不成功，因为pkgs.repoforge.org无法访问。于是想直接编译源代码的方式更新。在[git linux](https://git-scm.com/download/linux)页面找到[the IUS Community Project](https://ius.io/)项目，在[usage-guide](https://ius.io/Usage/#usage-guide)里找到使用方法。
```
yum install yum-plugin-replace
yum replace git --replace-with git2u
```
现在是2.9.1版本。

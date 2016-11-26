title: Python多版本环境管理之pyenv
date: 2016-11-26 11:30:04
tags:
    - Python
    - pyenv
    - virtualenvwrapper
categories:
---
之前使用[virtualenvwrapper](http://program.dengshilong.org/2016/04/21/%E4%BD%BF%E7%94%A8virtualenvwrapper%E9%9A%94%E7%A6%BBPython%E7%8E%AF%E5%A2%83/)来管理Python虚拟环境，使用Python2.7, 没发现问题。后来公司的新项目都使用Python3.5，此时virtualenvwrapper就不能满足需求了，于是开始使用[pyenv](https://github.com/yyuu/pyenv)。

总的来说, pyenv是用于管理Python版本，而virtualenv用于管理Python虚拟环境，两者结合使用，基本上能满足需求。

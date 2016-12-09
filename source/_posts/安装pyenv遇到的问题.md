title: 安装pyenv遇到的问题
date: 2016-12-09 23:09:44
tags:
    - Python
    - pyenv
categories:
---
在[Python多版本环境管理之pyenv](http://program.dengshilong.org/2016/11/26/Python%E5%A4%9A%E7%89%88%E6%9C%AC%E7%8E%AF%E5%A2%83%E7%AE%A1%E7%90%86%E4%B9%8Bpyenv/)中说到使用[pyenv](https://github.com/yyuu/pyenv), 但没有写安装的过程。本以为按照官网安装即可，后来在给同事安装时，发现了问题。

官网上说，在使用Zsh，需要将环境变量加到~/.zshenv中，而不是~/.bash_profile，但其实这样还是会提示没有安装pyenv。正确的配置是将环境变量加到~/.zshrc中。

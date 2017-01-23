title: Python之coverage使用
date: 2017-01-23 19:53:21
tags:
    - Python
    - coverage
categories:
---
coverage用来统计代码测试覆盖率，非常方便。

## 安装
执行`pip install coverage`即可

## 指定代码路径
希望coverage只去统计我们关心的代码，此时[--source](https://coverage.readthedocs.io/en/coverage-4.3.4/source.html#source-execution)选项派上用场。例如`coverage --source .`只统计当前目录下的所有代码。
## coveragerc配置
通过使用coverage配置文件，可以很方便的控制coverage。coverage默认使用.coveragerc里的配置，也可以通过--rcfile来配置。
## 统计数据输出
执行完coverage测试后，可以执行coverage report和coverage html输出统计信息。

完整的Django测试执行命令可以这样`coverage run --rcfile=.coveragerc --source . ./manage.py test`

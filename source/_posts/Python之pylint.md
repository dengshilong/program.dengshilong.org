title: Python之pylint
date: 2017-01-23 19:50:31
tags:
    - Python
    - pylint
    - Django
categories:
---
[pylint](https://pylint.readthedocs.io/en/latest/index.html)用于Python代码规范检查。默认代码风格遵循[PEP08](https://www.python.org/dev/peps/pep-0008/)

### 使用配置文件
配置文件可以通过如下命令生成
```
 pylint --generate-rcfile > .pylintrc
```
执行pylint时，可以通过指定--rcfile参数来加载配置文件。而默认配置文件加载顺序可以参考[命令行参数](https://pylint.readthedocs.io/en/latest/user_guide/run.html#command-line-options)这节。

### Django代码检查
对于Django, 有[pylint-django](https://github.com/landscapeio/pylint-django)这个pylint插件用来代码检查。`pip install pylint-djangop`安装后，添加--load-plugins参数即可启用，如`pylint --load-plugins pylint_django` 
### 警告忽略
有时pylint的检查不满足需求，太繁琐，此时可以忽略它。如在`for d in data:`里，会报Invalid variable错误，即[C0103](http://pylint-messages.wikidot.com/messages:c0103), 此时加上`# pylint: disable=C0103`可以忽略这个警告。

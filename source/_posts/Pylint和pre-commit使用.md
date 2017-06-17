title: Pylint和pre-commit使用
date: 2017-06-17 11:21:21
tags:
    - Python
    - Pylint
    - pre-commit
categories:
---
# Pylint
[Pylint](https://pylint.readthedocs.io/en/latest/index.html) 用于 Python 静态代码检查。默认代码风格遵循 [PEP08](https://www.python.org/dev/peps/pep-0008/)

## 安装
执行 `pip install pylint` 即可

## 使用配置文件
配置文件可以通过如下命令生成`pylint --generate-rcfile > .pylintrc`。执行 pylint 时，可以通过指定 --rcfile 参数来加载配置文件。而默认配置文件加载顺序可以参考[命令行参数](https://pylint.readthedocs.io/en/latest/user_guide/run.html#command-line-options)这节。例如，对当前目录下所有 Python 文件作代码检查，执行 `pylint --rcfile .pylintrc *.py` 即可

## Flask代码检查
对于Flask, 有[pylint-flask](https://github.com/jschaf/pylint-flask) 这个 Pylint 插件用来代码检查。`pip install pylint-flask`安装后，添加 --load-plugins 参数即可启用，如`pylint --load-plugins pylint_flask` 

## 警告忽略
有时 Pylint 的检查不满足需求，太繁琐，此时可以忽略它。如在`for d in data:`里，会报Invalid variable错误，即, 此时加上`# pylint: disable=invalid-name`可以忽略这个警告。暴力一点的方法是在文件开头添加`# pylint: disable=invalid-name`，这样会对整个文件忽略检查。更暴力的方法是修改 .pylintrc 文件，在disable这项里添加 invalid-name , 这样就会对所有文件忽略这个检查。

# pre-commit
[pre-commit](http://pre-commit.com/) 用来配置 commit 代码时检查代码。

## 安装
执行 `pip install pre-commit` 即可。

## 添加移除 git hooks
执行 `pre-commit install` , 将 pre-commit 添加到 git hooks 中

## 配置
在项目根目录下，添加.pre-commit-config.yaml文件即可进行配置，如下就是一个配置。

```
-   repo: https://github.com/pre-commit/pre-commit-hooks
    sha: v0.7.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
    -   id: autopep8-wrapper
    -   id: check-docstring-first
    -   id: check-json
    -   id: check-added-large-files
    -   id: check-yaml
    -   id: debug-statements
    -   id: requirements-txt-fixer
-   repo: https://github.com/pre-commit/pre-commit
    sha: v0.11.0
    hooks:
    -   id: validate_config
    -   id: validate_manifest
-   repo: local
    hooks:
    -   id: pylint
        name: pylint
        entry: pylint
        language: system
        files: \.py$
        exclude: test_gevent.py|app/rpc/notify_manager
        args: [--rcfile=.pylintrc, --load-plugins=pylint_flask]
```

此后，每次提交代码时，都会进行代码规范检查。

## 移除 git hooks
执行 `pre-commit uninstall`, 将 pre-commit 从git hooks中移除

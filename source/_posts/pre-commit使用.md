title: pre-commit使用
date: 2017-01-23 19:51:52
tags:
    - Python
    - pre-commit
categories:
---
为了保证团队成员提交的代码是符合规范的，可以使用[pre-commit](http://pre-commit.com/)来做代码检查。

### 安装
pre-commit安装很方便，执行`pip install pre-commit'即可。

### 添加到git hooks
执行`pre-commit install`, 将pre-commit添加到git hooks中
### 配置
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
        exclude: test_gevent.py
        args: [--rcfile=.pylintrc, --load-plugins=pylint_django]
```
此后，每次提交代码时，都会进行代码规范检查。

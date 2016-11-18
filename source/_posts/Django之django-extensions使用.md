title: Django之django-extensions使用
date: 2016-11-18 20:58:58
tags:
    - Django
categories:
---
前几天同事推荐了[djano-extensions](https://django-extensions.readthedocs.io/en/latest/)，说是用来执行一些Django脚本特别爽，尝试之后，果然如此。

在[RunScript](https://django-extensions.readthedocs.io/en/latest/runscript.html)里有编写脚步的方法，有了它，之后写脚本时不需要导入Django环境，因为django-extensions帮你做了，很不错。
```
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()
```

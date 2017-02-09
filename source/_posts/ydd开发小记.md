title: ydd开发小记
date: 2017-02-07 20:06:50
tags:
    - Python
    - ydd
categories:
---
在[ici，基于python的终端查词小工具](http://lazynight.me/3378.html)看到终端查词小工具，遗憾的是不能查中文，而这是我经常用的。尝试在ici上添加中文，没有搞定，于是决定自己写一个。因为经常使用有道词典，于是有了[ydd](https://github.com/dengshilong/ydd).

真正写起来还是比较简单，就是一个HTTP请求，之后读取JSON里的数据，显示出来。使用了[click](http://click.pocoo.org/5/)和[requests](http://docs.python-requests.org/en/master/)两个库后，很快就写好了。click提供命令行参数解析以及终端颜色显示，requests用来发起请求非常方便。考虑到是小工具，所以异常情况都没有处理，代码总共才70行。后来发现不能兼容2.7，于是加上[six](https://pythonhosted.org/six/)来判断Python版本。

之后是使用[setuptools](https://setuptools.readthedocs.io/en/latest/setuptools.html)发布到[pypi](https://pypi.python.org/pypi/ydd)上，很开心。目前使用上来说，查英文单词还是[ici](https://github.com/Flowerowl/ici)好，因为有例句，不过查中文当然是使用ydd好了。

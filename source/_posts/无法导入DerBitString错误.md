title: 无法导入DerBitString错误
date: 2018-10-11 16:38:20
tags:
    - Python
categories:
---
在安装Python包时，报如下错误
```
from Crypto.PublicKey import RSA
from Crypto.Util.asn1 import (DerSequence, DerInteger, DerBitString,
    
ImportError: cannot import name 'DerBitString' from 'Crypto.Util.asn1'
```

在网上只找到[ImportError: cannot import name 'DerBitString'](https://github.com/matlink/gplaycli/issues/147), 评论里说 Could you please try in a new virtualenv? It seems related to your virtualenv.

我使用的是pyenv搭建的Python3.6.2, 报错, 后来同事用virtualenv搭了个Python3.7.0的环境，不会报错。于是试了用pyenv搭建个Python3.7.0的环境，还是报错。于是可以确定是pyenv的原因，用virtualenvwarpper搭了个Python3.6.5的环境，这次没有报错。

用了这么久pyenv, 第一次遇到这种问题，莫名奇妙。

2018年11月23日更新: 发现原因了，是因为PyCrypto包和PyCryptodome有冲突，当只安装PyCrypto时就没有这个问题。事实上，最好使用PyCryptodome这个包，因为它是PyCrypto的替代者，只是这里应用依赖PyCrypto包，所以才用它。

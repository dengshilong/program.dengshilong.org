title: Python之logging等级困惑
date: 2017-04-06 21:51:53
tags:
    - Python
    - logging
categories:
---
日志是程序员的生命线，在Python中使用[logging](https://docs.python.org/2/library/logging.html)来记录日志。之前写过[Django配置logging](http://program.dengshilong.org/2016/07/24/Django%E4%B9%8Blogging/), 这次在Flask里配置日志。查看[Flask日志配置文档](http://flask.pocoo.org/docs/0.12/errorhandling/), 最后在一个日志等级上遇到问题。

给创建app时，添加日志配置
```
file_handler = RotatingFileHandler("lovehate.log")
file_handler.setLevel(logging.WARNING)
file_handler.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
app.logger.addHandler(file_handler)

```
之后使用app.logger.info输出日志，日志只在终端中显示，没有写到文件中。百思不得其解，叫同事过来看看，才发现是日志等级的原因。

以前一直认为INFO的等级比WARNING更高，所以一直认为上面的配置，应该会输出日志。后来看了文档才知道日志等级从高到低是DEBUG, INFO, WARNING, ERROR, CRITICAL。或许这还是不合理的，WARNING应该比INFO低才对啊。

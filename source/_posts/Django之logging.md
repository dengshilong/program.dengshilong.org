title: Django之logging
date: 2016-07-24 12:25:20
tags:
    - Django
    - logging
categories:
    - Python
---
对于一个应用来说，日志是很重要的一部分。Django提供的[logging](https://docs.djangoproject.com/ja/1.9/topics/logging/)功能，使用Python自带的[logging](https://docs.python.org/3/library/logging.html#module-logging)模块来处理系统日志很方便。

下面是一份简单的配置。配置最主要的需求是能够看到Django查询数据库的sql语句。

```
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format' : '%(levelname)s [%(asctime)s] [%(name)s:%(module)s:%(funcName)s:%(lineno)s] [%(exc_info)s] %(message)s',
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/debug.log',
            'formatter': 'standard'
        },
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

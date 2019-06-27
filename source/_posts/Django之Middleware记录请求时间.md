title: Django之Middleware记录请求时间
date: 2019-06-27 19:55:25
tags:
    - Django
categories:
---
前些天，监控系统那边提了需求，要求应用必须加上访问时长日志，并得知道是谁访问的，于是就想到了使用Django的Middleware. 请求进来的时候记下时间，返回的时候记下时间，两者相减，就是请求的时长。代码如下

```
import logging
import time
from datetime import datetime

from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class LoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        execute_time = time.time() - request.start_time
        path = request.path
        username = '-'
        method = request.method
        if hasattr(request, 'user') and not request.user.is_anonymous:
            username = request.user.username
        code = response.status_code
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        res = "{} {} {} {} {:.2f} {}".format(now, username, path, method, execute_time, code)
        logger.info(res)
        return response
```

之后在Django配置里，LOGGING->formatters里加上
```
very_simple:
    format: '%(message)s'
```
LOGGING->handlers里加上
```
monitor:
    level: 'INFO'
    class: 'logging.handlers.RotatingFileHandler'
    filename: 'monitor.log'
    formatter: 'very_simple'
```
在LOGGING->loggers里加上
```
 'helper.middleware.logging_middleware':
    handlers: ['monitor']
    level: 'INFO'
    propagate: False
```
其中helper.middleware.logging_middleware是LoggingMiddleware这个类的存放位置，

最后在项目settings的MIDDLEWARE的最前面加上'helper.middleware.logging_middleware.LoggingMiddleware'

如此日志就会输出到monitor.log


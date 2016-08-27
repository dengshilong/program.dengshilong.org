title: you-must-set-settings-allowed_hosts-if-debug-is-false
date: 2016-08-27 14:41:32
tags:
    - Django
    - celery
    - kombu
categories:
    - Python
---
某天，前端同事的Django项目无法启动，报`you must set settings.allowed_hosts if debug is false`错误，可是查看配置文件，明明设置debug=True, 不知为何。

找了好久，组长过来看了之后，发现是`Cannot import name _uuid_generate_random`错误，于是想到之前也遇到过这个问题，只是当时没有做笔记，所以印象不深。

按照[cannot-import-name-uuid-generate-random-in-heroku-django](
http://stackoverflow.com/questions/34198538/cannot-import-name-uuid-generate-random-in-heroku-django), 升级Kombu到3.0.30，依然提示这个错误，
之后按照[ImportError: cannot import name _uuid_generate_random](https://discuss.erpnext.com/t/importerror-cannot-import-name--uuid-generate-random/10748)的提示，升级celery, 执行`pip install --upgrade celery`，这次可以正常启动。

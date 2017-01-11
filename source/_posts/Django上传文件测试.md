title: Django上传文件测试
date: 2017-01-11 21:52:20
tags:
    - Django
    - Python
categories:
---
在编写测试时遇到表单上传文件的问题，问了同事后，给了stackoverflow上[how to unit test file upload in django](http://stackoverflow.com/questions/11170425/how-to-unit-test-file-upload-in-django)链接, 在[django.test.Client.post](https://docs.djangoproject.com/en/dev/topics/testing/tools/#django.test.Client.post)里看到如下例子

```
>>> c = Client()
>>> with open('wishlist.doc') as fp:
...     c.post('/customers/wishes/', {'name': 'fred', 'attachment': fp})
```
对于图片，需要加上rb模式，例子如下
```
>>> c = Client()
>>> with open('wishlist.png', 'rb') as fp:
...     c.post('/customers/wishes/', {'name': 'fred', 'attachment': fp})
```
解决问题。

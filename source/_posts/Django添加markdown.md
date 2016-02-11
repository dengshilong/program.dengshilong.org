title: Django添加markdown
date: 2016-02-10 21:18:52
tags:
  - Django 
  - markdown
categories:
  - Python
---
在[Django后台添加markdown编辑器](http://program.dengshilong.org/2014/06/22/Django后台添加markdown编辑器/)中说过如何在Django后台添加markdown编辑器,后来发现这里添加的pagedown有一个问题，也就是换行问题。在markdown中，单个换行会用空格代替，但pagedown中并没有这么做。经过跟踪，发现问题是在[pagedown-extra](https://github.com/jmcmanus/pagedown-extra)中,解决的办法是在[pagedown/Markdown.Converter.js](https://github.com/jmcmanus/pagedown-extra/blob/master/pagedown/Markdown.Converter.js)的_FormParagraphs函数1168行`//if this is an HTML marker, copy it`前添加`str = str.replace(/\n/g, " ");`即可.

如此，在后台添加markdown编辑器就完成了。之后还需要前台现实时也用markdown渲染,通过自定义filter,添加markdown渲染可以实现这个功能。

* `pip install markdown`安装markdown

* 按照[自定义模版标签和过滤器](https://docs.djangoproject.com/en/1.9/howto/custom-template-tags/), 在所在的app目录下新建templatetags目录，在templatetags目录里新建`__init__.py`文件，之后编写my_markdown.py文件，内容如下：
```
from django import template
from markdown import markdown
register = template.Library()
@register.filter(name='mark')
def mark(value):
    return markdown(value, extensions=['markdown.extensions.extra', 'markdown.extensions.codehilite'])
```
* 在模版中使用
```
{% load my_markdown %}
  <p>{{ post.content|mark|safe}}</p> 
```










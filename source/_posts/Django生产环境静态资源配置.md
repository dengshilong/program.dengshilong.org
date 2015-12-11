title: Django生产环境静态资源配置
tags:
  - Django
  - 静态资源
id: 760
categories:
  - Python
date: 2014-06-22 00:17:22
---

在开发环境中，使用Django自带的server,css这些静态资源都能够找到，可是用了gunicorn后,就找不到css等静态资源了，不知道如何是好，只记得之前看到在什么地方提到开发环境和生产环境是存在一些差异的。问过志容，志容说是要配置Nginx，可是我用gunicorn,根本都没有通过nginx。

今天正好看文档，正好看到，于是记下来。在https://docs.djangoproject.com/en/dev/howto/static-files/这个页面里有说到如何设置。

*   Set the [<tt class="xref std std-setting docutils literal"><span class="pre">STATIC_ROOT</span></tt>](https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-STATIC_ROOT) setting to the directory from which you’d like to serve these files, for example:

<div class="highlight-python">
<div class="highlight">
<pre><span class="n">STATIC_ROOT</span> <span class="o">=</span> <span class="s">"/var/www/example.com/static/"</span>
</pre>
</div>
</div>
*   Run the [<tt class="xref std std-djadmin docutils literal"><span class="pre">collectstatic</span></tt>](https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#django-admin-collectstatic) management command:

<div class="highlight-python">
<pre>$ python manage.py collectstatic</pre>
</div>
为了避免硬编码，将STATIC_ROOT设置为os.path.join(BASE_DIR, 'static')后，

运行python manage.py collectstatic即可
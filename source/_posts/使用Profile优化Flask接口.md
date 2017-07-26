title: 使用Profile优化Flask接口
date: 2017-07-25 21:16:36
tags:
    - Profile
    - Flask
categories:
---
项目里有一个脚本列表接口响应非常慢，需要10秒以上，看程序，认为是访问数据库过多，优化之后还是很慢。继续看代码，没看出什么名堂。同事推荐使用 Profile 看看，于是使用，解决了问题。

根据 [Profiling a Werkzeug (flask) app](http://www.alexandrejoseph.com/blog/2015-12-17-profiling-werkzeug-flask-app.html) 这篇文章，在代码里加上

```
from werkzeug.contrib.profiler import ProfilerMiddleware
from myapp import app  # This is your Flask app
app.wsgi_app = ProfilerMiddleware(app.wsgi_app)
app.run(debug=True)    # Standard run call
```

再次调用接口时，终端上就显示了一些调用信息，根据这些信息去代码里找原因，解决问题。

最后发现是接口里返回的最后修改时间和修改原因都是从 git 仓库里访问，脚本多的话，就很慢了。将这两个信息保存在数据库中就可以解决问题。

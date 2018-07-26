title: ES6中的箭头函数
date: 2018-07-12 19:24:40
tags:
    - JavaScript
categories:
---
在使用axios来进行Ajax请求时遇到这个问题。

使用如下代码向后端API请求时，无法对posts赋值，this是undefined

```
fetchPost() {
  axios.get('http://127.0.0.1:7001/api/blog/posts/')
    .then(function (response) {
      console.log(response);
      console.log(this);
      this.posts = response.data.results
    })
    .catch(error => {
      // handle error
      console.log(error);
    })
}
```

于是改成Vue教程中[使用 axios 访问 API](https://cn.vuejs.org/v2/cookbook/using-axios-to-consume-apis.html)的箭头函数，这次可以得到结果。

```
fetchPost() {
  axios.get('http://127.0.0.1:7001/api/blog/posts/')
    .then(response => {
      console.log(response);
      console.log(this);
      this.posts = response.data.results
    })
    .catch(error => {
      // handle error
      console.log(error);
    })
}
```
在[深入浅出ES6（七）：箭头函数 Arrow Functions](http://www.infoq.com/cn/articles/es6-in-depth-arrow-functions)里写到，普通function函数和箭头函数的行为有一个微妙的区别，箭头函数没有它自己的this值，箭头函数内的this值继承自外围作用域。原来如此。

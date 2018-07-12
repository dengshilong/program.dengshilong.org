title: "vue-router去除#"
date: 2018-07-12 20:07:19
tags:
categories:
---
在使用vue-router时，URL中总会有多了个#, 看着总是不爽，而且多了这个符号，以前被搜索引擎收录的页面就无法访问了，于是想办法去除。在Vue的文档中[HTML5 History 模式](https://router.vuejs.org/zh/guide/essentials/history-mode.html)找到了解答，也就是添加history模式即可。

```
const router = new VueRouter({
  mode: 'history',
  routes: [...]
})
```

看到[警告](https://router.vuejs.org/zh/guide/essentials/history-mode.html#%E8%AD%A6%E5%91%8A)中说，这么做以后，服务器就不再返回 404 错误页面，因为对于所有路径都会返回 index.html 文件。为了避免这种情况，你应该在 Vue 应用里面覆盖所有的路由情况，然后在给出一个 404 页面。

```
const router = new VueRouter({
  mode: 'history',
  routes: [
    { path: '*', component: NotFoundComponent }
  ]
})
```

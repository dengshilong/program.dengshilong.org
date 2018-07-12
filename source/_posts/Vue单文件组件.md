title: Vue单文件组件
date: 2018-07-13 00:41:10
tags:
    - Vue
categories:
---
实现文章列表时，写了如下组件

```
const axios = require('axios');
var ComponentBlog = {
  props: ['post'],
  template: `
    <div class="blog-post">
      <h3>{{ post.title }}</h3>
      <div v-html="post.content"></div>
    </div>
  `
  }
export default {
  components: {
    'blog-post': ComponentBlog 
  },
```

但是希望组件能够在其它页面复用，于是放在一个文件中，然后导入进来。在这里，我放在BlogPost.vue中，文件内容如下

```
<template>
  <div class="blog-post">
    <h3>{{ post.title }}</h3>
    <div v-html="post.content"></div>
  </div>
</template>
```

然后编写如下代码使用组件

```
<template>
  <div>
    <blog-post v-for="post in posts" :key="post.id" :post="post"></blog-post>
  </div>
</template>

<script>
import BlogPost from '@/components/BlogPost'
const axios = require('axios');
export default {
  components: {
    BlogPost
  },
  data () {
    return {
      posts: [],
    }
  },
  created() {
      this.fetchPost();
  },
  methods: {
    fetchPost() {
      axios.get('http://127.0.0.1:7001/api/blog/posts/')
        .then(response => {
          console.log(response)
          console.log(this)
          this.posts = response.data.results
        })
        .catch(error => {
          // handle error
          console.log(error);
        })
    }
  }
}
</script>
```

但是一直报post是未定义的。问过同事后，才知道在Vue文档中，有介绍[单文件组件](https://cn.vuejs.org/v2/guide/single-file-components.html)的使用方法。于是将BlogPost.vue改成如下内容

```
<template>
  <div class="blog-post">
    <h3>{{ post.title }}</h3>
    <div v-html="post.content"></div>
  </div>
</template>

<script type="text/javascript">

export default{
  props: {
    post: Object
  },
  data(){
    return {
    }
  },
  created(){
  },
  methods: {
  },
}
</script>
```

这样之后，组件就可以正常使用了。

title: Chrome开发者工具-前端开发利器
date: 2017-04-10 13:29:22
tags:
    - Chrome
    - AJAX
categories:
---
最近做前端开发，发现Chrome开发者工具真是前端开发的一大利器。这里做个简单记录。

Chrome在Mac上, 可以使用快捷键Option + Command + I打开开发者工具。查看源码是Option + Command + U。

Network标签下，有一个XHR请求，XHR代表XMLHttpRequest，所以简单来说，就是AJAX请求。

Chrome的一大功能是可以修改Javascript文件中的代码，保存后就可以生效。这是一个非常有用的功能，在表单提交时，如果Javascript出错，一般来说是去修改源文件，然后重新加载，然后填入表单字段，重新提交。这种方式，需要反复填入表单，如果表单字段很多，则非常麻烦。有了Chrome这个功能后，直接修改source标签下的Javascript文件，保存后即可生效，然后就可以提交，这样非常方便。

需要注意的是，修改source下的js文件，并不会修改源代码，调试完成后，还需要将修改同步到源文件中。


## 参考资料
* [AJAX - 向服务器发送请求](http://www.w3school.com.cn/ajax/ajax_xmlhttprequest_send.asp)
* [使用 Chrome 开发者工具进行 JavaScript 问题定位与调试](https://www.ibm.com/developerworks/cn/web/1410_wangcy_chromejs/)
* [前端开发神一样的工具chrome调试技巧](http://colinued.leanote.com/post/%E5%89%8D%E7%AB%AF%E5%BC%80%E5%8F%91%E7%A5%9E%E4%B8%80%E6%A0%B7%E7%9A%84%E5%B7%A5%E5%85%B7chrome%E8%B0%83%E8%AF%95%E6%8A%80%E5%B7%A7)

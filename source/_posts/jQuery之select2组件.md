title: jQuery之select2组件
date: 2017-05-13 10:37:45
tags:
    - jQuery
    - select
categories:
---
select2组件用来替代select, 它的一个最常用功能是搜索功能。

编写如下简单测试代码，可以看看搜索功能
```
<html>
<head>
<link href="https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.3/css/select2.min.css" rel="stylesheet" />
</head>
<body>

    <select class="js-example-basic-single">
      <option value="AL">Alabama</option>
      <option value="WY">Wyoming</option>
    </select>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.3/js/select2.min.js"></script>

    <script type="text/javascript">
    $(document).ready(function() {
      $(".js-example-basic-single").select2();
    });
    </script>
</body>
```

使用过程中遇到的一个问题是，当改变了select2的值时，改变后的结果没有显示在页面上。在[select2 FAQ](https://select2.github.io/options.html#what-events-does-select2-listen-for)里有说到这个问题，需要触发change事件。如果只想把change事件限定在select2内，可以使用`$('select').trigger('change.select2');`

title: jQuery常用问答
date: 2017-05-27 17:18:56
tags:
    - jQuery
categories:
---
使用jQuery操作时，发现[jQuery常用问答](http://learn.jquery.com/using-jquery-core/faq/), 都是一些很使用的功能。

## 如何设置或取消一个checkbox或者radio按钮

这里主要用到prop方法

```
// 设置 #x
$( "#x" ).prop( "checked", true );
 
// 取消 #x
$( "#x" ).prop( "checked", false );

// 获取是否选择 #x
$('#x').prop("checked")
```


## 如何从select框中获取所选项的值和文本

```
<select id="myselect">
    <option value="1">Mr</option>
    <option value="2">Mrs</option>
    <option value="3">Ms</option>
    <option value="4">Dr</option>
    <option value="5">Prof</option>
</select>
```

这里主要是val和text方法
```
// 获取值
$( "#myselect" ).val();

// 获取文本
$( "#myselect option:selected" ).text();
```

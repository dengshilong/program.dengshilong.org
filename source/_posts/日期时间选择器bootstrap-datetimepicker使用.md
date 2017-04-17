title: 日期时间选择器bootstrap-datetimepicker使用
date: 2017-04-17 21:52:10
tags:
    - Bootstrap
categories:
---
时间日期选择器可以使用[bootstrap-datetimepicker](https://github.com/smalot/bootstrap-datetimepicker), 中文文档见[Bootstrap日期和时间表单组件](http://www.bootcss.com/p/bootstrap-datetimepicker/index.htm)

使用时有一些注意点，其中一点是不要使用datetimepicker class, 会出bug，主要现象是两个时间框叠在一起。

对于不同的时间输入框，要独立初始化，如下面两个输入框

```
<div class="row">
    <label for="begin-time" class="col-sm-2 control-label">开始时间</label>
    <div class="col-sm-4">
        <input id="begin-time" readonly type="text" class="form-control" data-date-format="yyyy-mm-dd hh:ii:ss">
    </div>
</div>
<div class="row">
    <label for="end-time" class="col-sm-2 control-label">结束时间</label>
    <div class="col-sm-4">
        <input id="end-time" readonly type="text" class="form-control" data-date-format="yyyy-mm-dd hh:ii:ss">
    </div>
</div>
```

要像如下独立初始化
```
$('#begin-time').datetimepicker({
    language: 'zh-CN'
});
$('#end-time').datetimepicker({
    language: 'zh-CN'
});
```

对于中文，还需要加载ootstrap-datetimepicker.zh-CN.js

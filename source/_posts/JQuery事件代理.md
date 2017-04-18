title: JQuery事件代理
date: 2017-04-18 10:58:46
tags:
    - JQuery
categories:
---
JQuery的事件代理主要用来解决通过js添加的HTML元素无法监听事件的问题。

在[JQuery event delegation](https://learn.jquery.com/events/event-delegation/)中给了如下一个简单例子，

```
<html>
    <head>
        <script src="http://cdnjs.cloudflare.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
    </head>
    <body>
        <div id="container">
            <ul id="list">
                <li><a href="http://domain1.com">Item #1</a></li>
                <li><a href="/local/path/1">Item #2</a></li>
                <li><a href="/local/path/2">Item #3</a></li>
                <li><a href="http://domain4.com">Item #4</a></li>
            </ul>
        </div>
        <script>
            $( "#list a" ).on( "click", function( event ) {
                event.preventDefault();
                console.log( $( this ).text() );
            });
            $( "#list" ).append( "<li><a href='http://newdomain.com'>Item #5</a></li>" );
        </script>
    </body>
</html>
```

点击item1到item4，对于click事件都会有响应，在console中可以看到输出，而点击item5时click事件不会响应，这是因为将click事件绑定时，item5还没有生成。

解决这个问题的方法是使用事件代理，原理是利用了事件传播机制。也就是在某一个元素中的事件，如果没有得到处理，一直会向父节点触发，直到根节点。如上面的a元素的click事件，如果没有被捕获，一直会向上触发，路径如下

* `<a>`
* `<li>`
* `<ul #list>`
* `<div #container>`
* `<body>`
* `<html>`
* document root

在`<ul #list>`元素上添加click事件，就可以看到效果。
```
$( "#list" ).on( "click", function( event ) {
    event.preventDefault();
    console.log( $( this ).text() );
});
```

最后，如果使用事件代理，我们可以把它绑定到`<ul #list>`元素，然后通过'a'去找到`<a>`元素，这样就可以监听通过js添加的HTML元素。
```
$( "#list" ).on( "click",  'a', function( event ) {
    event.preventDefault();
    console.log( $( this ).text() );
});
```

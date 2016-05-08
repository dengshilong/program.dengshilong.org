title: 给sphinxclient.c增加flush索引到硬盘功能
tags:
  - flush
  - Sphinx
  - sphinxclient
  - 开源
  - 索引
id: 799
categories:
  - 搜索引擎
date: 2014-07-11 11:35:02
---

在Sphinx中，如果你调用的是C的api，并使用更新属性的功能，而此时，你想将更新后的索引冲刷到硬盘，你就会发现C的api中没有提供这个功能。而在Java,PHP,Python中，都提供了FlushAttributes这个接口来完成这个功能，于是你不得不另外在写一个程序来调用这个接口。

仔细想想，Sphinx都是用C++写的，而C的API中竟然没有提供这个接口，反倒是其它语言有提供，真是匪夷所思。所幸，代码都是开源的，想要自己有这个接口，自己动手写一个就好了，也许这就是开源的好处。

代码如下：
``` 
int sphinx_flush_attributes(sphinx_client * client) {
    char *buf, *req, *p;
    int req_len = 0;
    if (!client) {
        printf("not valid client\n");
        return -1;
    }
    buf = malloc ( 12 + req_len ); // request body length plus 12 header bytes
    if ( !buf ) {
        set_error ( client, "malloc() failed (bytes=%d)", req_len );
        return -1;
    }

    req = buf;

    send_word ( &req, SEARCHD_COMMAND_FLUSHATTRS );
    send_word ( &req, VER_COMMAND_FLUSHATTRS );
    send_int ( &req, req_len );

    // send query, get response
    if ( !net_simple_query ( client, buf, req_len ) )
        return -1;

    // parse response
    if ( client->response_len < 4 ) {
        set_error ( client, "incomplete reply" );
        return -1;
    }

    p = client->response_start;
    return unpack_int ( &p );
}
```
之后还要添加
SEARCHD_COMMAND_FLUSHATTRS  = 7，
VER_COMMAND_FLUSHATTRS  = 0x100，
以及在头文件中添加int sphinx_flush_attributes(sphinx_client * client)；即可。

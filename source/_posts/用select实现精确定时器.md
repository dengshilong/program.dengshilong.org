title: 用select实现精确定时器
tags:
  - select
  - SIGINT
  - sleep
  - 中断
  - 定时器
  - 忽略
id: 587
categories:
  - 编程
date: 2013-12-26 21:37:40
---

之前为了找出Sphinx中index 'test1': search error: query too complex, not enough stack (thread_stack=1217498K or higher required)这个bug,大致看了一下Sphinx的源码，发现问题的原因是在计算线程使用的空间时出错，具体原因依然没有找到，还在努力当中。在这个过程中，看到以下这段程序
``` c
void sphSleepMsec ( int iMsec )
{
    if ( iMsec<0 )
        return;

#if USE_WINDOWS
    Sleep ( iMsec );

#else
    struct timeval tvTimeout;
    tvTimeout.tv_sec = iMsec / 1000; // full seconds
    tvTimeout.tv_usec = ( iMsec % 1000 ) * 1000; // remainder is msec, so *1000 for usec

    select ( 0, NULL, NULL, NULL, &tvTimeout ); // FIXME? could handle EINTR
#endif
}
```
其实就是一个毫秒定时器，《UNIX环境编程》第14章的习题就要求实现一个这样的函数。看这段程序，又是令人恶心的匈牙利命名，把它改为正常点的比较好。程序中的注释"//FIXME?could handle EINR"说的是select会被SIGINT信号中断，那么这个定时器也会因为这个原因而被中断信号中断，看看能否提供不被中断的方法。立刻就想到了忽略中断信号，试了一下，其实还是挺容易的。难道这种直接忽略中断信号还是存在问题？
``` c
#include <sys/select.h>
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
void sleep_ms(int msec) {//睡眠msec毫秒
    if (msec < 0)
        return;
    signal(SIGINT, SIG_IGN);
    struct timeval tv; 
    tv.tv_sec = msec / 1000;//除以1000，得到秒数
    tv.tv_usec = (msec % 1000) * 1000;//得到剩余的毫秒数，之后乘以1000得到微秒数
    select(0, NULL, NULL, NULL, &tv);
}
int main() {
    printf("start sleeping\n");
    sleep_ms(4000);
    printf("finish sleeping\n");
    return 0;
}
```

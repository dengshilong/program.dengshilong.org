title: Python模块之blinker
date: 2017-04-19 14:02:51
tags:
    - Python
    - blinker
categories:
---
Flask使用[blinker](https://github.com/jek/blinker)来处理信号订阅和发送, 查看文档[blinker](https://pythonhosted.org/blinker/)看看简单的使用方法。

```
from blinker import signal

def subscriber(sender):
    print("Got a signal sent by %r" % sender)


class Processor:
    def __init__(self, name):
        self.name = name

    def go(self):
        ready = signal('ready')
        temp = ready.send(self)
        print(temp)
        print("Processing.")
        complete = signal('complete')
        complete.send(self)

    def __repr__(self):
        return '<Processor %s>' % self.name

ready = signal('ready')
ready.connect(subscriber)
temp = ready.send('sdfsdf')
print(temp)
processor_a = Processor('a')
processor_a.go()
```

使用signal创建一个信号, connect添加一个订阅，send发送信号，send的返回值是一个数组，数组元素是元祖，包含信号接收者和信号接收后的返回结果。

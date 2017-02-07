title: Chrome之JSON解析错误原因查找
date: 2017-02-07 19:35:36
tags:
    - Chrome
    - JSON
categories:
---
好好的Chrome，在上传文件时，换回结果是text/plain类型时，突然报这个错，VM7369:1 Uncaught SyntaxError: Unexpected token ( in JSON at position 0，而其它浏览器就没有这个问题。

刚开始以为是版本太新的原因，于是改用低版本，发现问题还是存在，看同事的Mac，不存在这个问题。

最后在前端同事的帮助下，知道Chrome的隐身模式，在Chrome隐身模式下没有这个问题，于是猜测是插件问题。最终锁定是
LastPass: Free Password Manager这个插件的原因。禁用后就没有这个问题。

title: 听说你Selenium和Playwright自动化无敌，来试试这两个站点吧
date: 2026-01-15 19:25:03
tags:
    - 自动化
    - 爬虫
categories:
---
有道友说遇到一个 Selenium 自动化过不去的站点 aHR0cHM6Ly93d3cuemhpcGluLmNvbS9qb2JfZGV0YWlsLzgyOTI2ZjM5MDRhNjZlMDUwM1pfMHQtLUZWUlMuaHRtbA==，又有道友说遇到了一个 Playwright 过不去的 aHR0cHM6Ly9zc28uY25pcGEuZ292LmNuL2FtLyMvbG9naW4=，于是掏出自动化工具试试，毕竟之前一直认为自动化在国内无敌。

在 Selenium和Playwright 自动化工具里加上--disable-blink-features=AutomationControlled参数(这个参数在[一个非常好用的自动化参数](http://program.robinjia.cc/2025/12/23/%E4%B8%80%E4%B8%AA%E9%9D%9E%E5%B8%B8%E5%A5%BD%E7%94%A8%E7%9A%84%E8%87%AA%E5%8A%A8%E5%8C%96%E5%8F%82%E6%95%B0/)里写过， 不知道的可以看看)后，打开网站后都会被重定向到空白页， 这可如何是好。
既然 Selenium 和 Playwright 自动化都过不去，那就试试 DrissonPage 了，好在 DrissonPage 能过。但究竟 Selenium 和 Playwright 为啥过不去呢，这是个问题。

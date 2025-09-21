title: 第一次遇到uniapp逆向
date: 2025-09-21 19:04:47
tags:
    - APP
    - 逆向
    - uniapp
    - JavaScript
categories:
---
道友遇到一个无壳APP，有个加密token不知道怎么生成的，jadx反编译之后也搜索不到参数，于是请教我怎么搞。猜测有可能是在JavaScript里，因为之前遇到过一个Weex开发的APP，也是怎么搜索都找不到加密参数，最后在JavaScript里找到了。

那次Weex开发的APP，找了老半天都不知道咋回事，后面是通过hook string还是hook url的办法，发现它会去下载一个JavaScript脚本，也就是 app-service.js，在这个脚本里才找到了加密参数。

于是道友就去找JavaScript代码，在反编译的apk里的assets目录里，找到了一个 uniapp 开发的app-service.js，在代码里找到了相关接口，但还是找不到相关的加密参数。于是道友又困惑了，只好来请教我。

此时我才知道这是使用 uniapp 开发的APP，于是去应用宝里下载了一个apk, 安装后发现它提示APP需要更新，点击更新后，APP又去下载了一些东西。拿着apk 里的 app-service.js 看了之后，接口确实都有，怎么会没有参数呢？想到刚才 APP 提示更新，莫非是会更新了uniapp? 于是去找APP临时目录，在/data/data目录下找到 APP对应的目录，在里面找到了一个app-service.js, 和apk里的app-service.js 大小不一样，搜索加密参数，果然在这里。剩下的就交给道友去解决了。

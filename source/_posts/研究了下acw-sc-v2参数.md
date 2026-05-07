title: 研究了下acw_sc__v2参数
date: 2026-05-07 09:22:50
tags:
    - 逆向
categories:
---
目标网址: aHR0cHM6Ly90cmFjay55dzU2LmNvbS5jbi9jbi9xdWVyeWRlbD9udW1zPVVLNDc1MDk1MDA4WVAmY3lwPWYxMDlhYTNhOGRhZmQ0NTM1YjcyZWZlODI4OTg4YjJk

最近acw_sc__v2这个参数更新了，看大家都在搞，于是也去看了一下。先用jsdom补环境试了下，直接秒了。后来又看了下算法，在遗心佬的[某某网站acw_sc_v2参数分析](https://mp.weixin.qq.com/s/3bocJB6KWsFwFtfiqk2P8A)里，已经有了详细的介绍，抠下来也不难。文章里有一点小错误，算法主体里的 q && (( G % 2) != 0) 应该是q && G % 2 == 0，不过这个不影响大局，测试下来都能过。最后借助AI，将JavaScript算法代码转成Python算法代码，跑起来更舒服了。

后来看到K哥写的[某坤行 1101，雪球 1038，新 acw_sc__v2 逆向分析](https://mp.weixin.qq.com/s/Wr2KjI8BOmMeQMJ1WuCE2A)，这几个参数的混淆有点类似，都是ob混淆类，于是就想着研究下混淆代码还原，毕竟从业以来还没正经写过ob混淆的插件。

先看看有没有现成的，打开蔡老板的星球，抄了好几个插件，最后就剩3个插件没找到。蔡老板星球的插件实在太多了，有时候真不知道要怎么找插件，主要是不知道搜啥关键词。正好土木佬的[某招投标服务平台AST详解](https://mp.weixin.qq.com/s/chCeOKP5z7ar9BkTIUG0FA)里有这三个插件，抄过来直接用了。

还原代码后再扣了一遍算法，舒服多了。也去试了下某坤行 1101，一样简单。混淆代码还是还原后调试起来舒服，属实事半功倍了。

##参考资料
* 某某网站acw_sc_v2参数分析 https://mp.weixin.qq.com/s/3bocJB6KWsFwFtfiqk2P8A
* 某招投标服务平台AST详解 https://mp.weixin.qq.com/s/chCeOKP5z7ar9BkTIUG0FA
* 【JS逆向百例】某坤行 1101，雪球 1038，新 acw_sc__v2 逆向分析 https://mp.weixin.qq.com/s/Wr2KjI8BOmMeQMJ1WuCE2A


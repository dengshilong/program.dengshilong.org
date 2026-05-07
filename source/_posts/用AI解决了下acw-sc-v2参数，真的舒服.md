title: 用AI解决了下acw_sc__v2参数，真的舒服
date: 2026-05-07 09:19:49
tags:
    - 逆向
categories:
---
去年写过[研究了下acw_sc__v2参数](https://mp.weixin.qq.com/s/B1m8wBkS-PSlHFIWw3fGow)，那时还要自己写AST，自己分析代码，今年可以直接用AI解决了。

把代码页面下载到本地后(也可以不用下载到本地，直接对着网站页面跑)，在页面目录启动个server, python3 -m http.server 8994, 然后让AI干活(这里我用的是GPT-5.4, 并安装好了chrome-devtools-mcp， 之前买过Claude中转站服务，结果被降智换模型了，没法用了), 使用chrome-devtools-mcp打开http://127.0.0.1:8994/ 并进行动态调试，找出cookies里acw_sc__v2参数的生成方法，并给出最终的Python代码。之后AI就猛猛干了，十几分钟就写好了Python代码，测试后能过(虽然代码不太对劲， 没有对random进行改变)。

之后分步走，先用AST解混淆，再找到参数生成算法。AI直接把1000多行的ob混淆代码还原成了200多行代码，和明文一样了，在这基础上，又让AI找出参数，几分钟后就写好了Python代码，测试也能过。

这太舒服了，想想20年刚入行那会一个ob就难住了，现在用AI直接拿捏，时代真的变了。听闻道友公司裁员，整个分公司直接没了，业务调整加上AI变强。这是最好的时代，这是最坏的时代。


title: '解决Error: searchd error: offset out of bounds问题'
tags:
  - max_matches
  - SetLimits
  - Sphinx
id: 716
categories:
  - 搜索引擎
date: 2014-05-06 19:42:39
---

因为项目需要用到分页功能，所以需要用到SetLimits函数，结果就出现了Error: searchd error: offset out of bounds (offset=9500, max_matches=1000)

于是找原因，发现配置文件中有max_matches这个选项，于是将它改为10000,可是依然出现Error: searchd error: offset out of bounds (offset=9500, max_matches=1000)错误，真是莫名其妙的错误，仔细看了SetLimits的函数说明以及SphinxClient.java,才知道使用SetLimits这个函数时，如果没有提供max_matches这个参数的值，则max_matches默认为1000,而9500超过了1000,所以溢出了。

现在终于明白原因，也就是说使用Sphinx一共可以在两个地方设置max_matches,一个是在searchd,也就是引擎端，提供给searchd的配置文件中进行设置；而在SphinxClient中,也就是客户端，如果在SetLimits函数中没有设置max_matches,则默认使用1000.这里有一点需要注意的是，客户端的max_matches一定要小于服务器端，否则会报错。而offset也一定要小于客户端的max_matches,这样offset才不会溢出。
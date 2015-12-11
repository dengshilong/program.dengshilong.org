title: 追踪query too complex not enough stack错误
tags:
  - Sphinx
  - Sphinx-for-chinese
  - sql_query_info
  - 匈牙利
id: 702
categories:
  - 搜索引擎
date: 2014-04-24 21:37:21
---

很早之前，在使用Sphinx搭建搜索服务时，遇到这个问题，到Sphinx for Chinese的群里请教，没有得到满意的答案，于是将sql_query_info 这个选项注释掉，就没有报错了。今天正好有时间，于是着手找到这个问题的症结，也算是为Sphinx做点贡献。

打开源代码，才发现用的是匈牙利命名法，看得不爽。也许因为没有Lucene那么出名，只有两个人在维护这个项目，代码里到处充斥这Fix Me,还好结构还算精良，要不然真不知道从和看起。本来想用GDB调试的，还不太熟练，于是就只好用最原始的printf输出。经过缩小范围，找到了一些蛛丝马迹，
在search.cpp中  的第331附近，主要的查询工作就在这里完成的，跳转过去之后
 if ( !pIndex->MultiQuery ( &tQuery, pResult, 1, &pTop, NULL ) )
锁定了到下面这个函数
在sphinx.cpp中 17301 if ( !sphCheckQueryHeight ( tParsed.m_pRoot, pResult->m_sError ) )
继续跳转，到了下面这行
在sphinx.cpp中 16404 int64_t iQueryStack = sphGetStackUsed() + iHeight*SPH_EXTNODE_STACK_SIZE;
输出之后，发现问题出在sphGetStackUsed这个函数里
在sphinxstd.cpp 中  1218行 int64_t sphGetStackUsed()
继续跳转，
sphinxstd.cpp 中  1221行
BYTE cStack;
 BYTE * pStackTop = (BYTE*)sphMyStack();
线程栈的使用大小就是上面两个值的差，继续查找
在sphinxstd.cpp return sphThreadGet ( g_tMyThreadStack );

这里用到了线程私有数据，看到私有数据的设置还是很正常，所以依然不知道哪里出了问题。于是索性将
int64_t iQueryStack = sphGetStackUsed() + iHeight*SPH_EXTNODE_STACK_SIZE;
这行改成
int64_t iQueryStack =  iHeight*SPH_EXTNODE_STACK_SIZE;
这样sql_query_info就可以使用了，也不会再报query too complex not enough stack错误。
可是这个自己查询得到的中文显示出来都是乱码，我认为是没有设置SET NAMES utf8的原因，但又无法在sql_query_info这里添加这句。虽然在sql_query_pre = SET NAMES utf8已经设置了，但是因为不是同一个查询连接，所以无效。

所以最终我得到解决这个错误的结论，那就是注释掉sql_query_info这个选项。最坑人的是，官方的示例中是开启这个选项的。
title: Sphinx更新属性无法为负值
tags:
  - Sphinx
  - 更新
  - 负值
id: 929
categories:
  - 搜索引擎
date: 2014-10-19 12:36:08
---

离职已经三个多月了，关于Sphinx的知识都快忘的差不多了，所以得赶紧记下来，以备不时之需。

离职前，在Sphinx-for-Chinese讨论组里异常活跃，很热心帮助群里的人解决问题。其中有个问题就是属性更新时无法设置为负值。于是看看Sphinx的更新属性流程。从searchd.cpp的main函数开始,到ServiceMain，TickPreforked,HandleClient,HandleClientSphinx,HandleCommandUpdate在这里看到
``` 
ARRAY_FOREACH ( i, tUpd.m_dAttrs )
{
    tUpd.m_dAttrs[i] = tReq.GetString().ToLower().Leak();
    tUpd.m_dTypes[i] = SPH_ATTR_INTEGER;
    if ( iVer>=0x102 )
    {     
        if ( tReq.GetDword() )
        {     
            tUpd.m_dTypes[i] = SPH_ATTR_UINT32SET;
            bMvaUpdate = true;
        }     
    }     
}
```
也就是说，这里默认是SPH_ATTR_INTEGER，而在Sphinx里，这个是无符号整型。因为在后面的一个判断语句里，有如下句子
``` 
} else
{     
    tUpd.m_dPool.Add ( tReq.GetDword() );
} 
```  
查看GetDword()，就可以知道返回的是无符号整型。

之后跳转到DoCommandUpdate,UpdateAttributes
在其中发现这样一句话：
// this is a hack
 // Query parser tries to detect an attribute type. And this is wrong because, we should
 // take attribute type from schema. Probably we'll rewrite updates in future but
 // for now this fix just works.
 // Fixes cases like UPDATE float_attr=1 WHERE id=1;
也就是说，Sphinx更新属性时，没有去读取配置文件。而只是根据上面代码中的设定去读取更新信息，所以没有办法读取负数。一个主要的原因是，Sphinx没有32位整型数据的概念，只有32位无符号整型的概念。

因为这样，你也许会尝试将要更为负值的字段设置成64位整型，因为这个是有正负的，可是尝试之后还是不行。这是因为在代码里，没有根据配置文件去读数据，所以它还是按照上面的设定去读数据，这样还是无符号的。所以对于这个问题，还有待Sphinx的开发人员去解决.

太久没用vim看代码了,连ctags的跳转是ctrl + ] 和ctrl + o都快忘记了。

title: Sphinx使用一元分词
tags:
  - Sphinx
  - Sphinx-for-chinese
  - 一元分词
id: 694
categories:
  - 搜索引擎
date: 2014-04-14 13:19:15
---

之前说过用Sphinx给同事搭建搜索服务，可是他提了一个要求，也就是文本中有牛皮癣这个词，搜牛皮时也要能搜到牛皮癣，这个要求在经过分词后是不可以完成的。于是只好去寻求一元分词和二元分词的办法。
在[http://lutaf.com/157.htm](http://lutaf.com/157.htm) 这里看到，“sphinx只要把min_word_len设置为1,并配置charset_table,默认就是单字切分 ”于是试着配置，结果不行。于是只好看文档，在文档中找到，默认情况下，Sphinx已经支持一元分词。
只需设置
charset_type = utf-8 ，
 ngram_len = 1，
ngram_chars = U+3000..U+2FA1F
这样，再次搜牛皮时，就可以搜到牛皮癣了。

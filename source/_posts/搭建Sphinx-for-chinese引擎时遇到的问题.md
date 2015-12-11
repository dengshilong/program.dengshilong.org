title: 搭建Sphinx-for-chinese引擎时遇到的问题
tags:
  - Klist
  - Sphinx
  - Sphinx-for-chinese
id: 668
categories:
  - 搜索引擎
date: 2014-04-11 09:00:08
---

在[关于sphinx引擎的一些想法](http://program.dengshilong.org/2014/04/11/关于sphinx引擎的一些想法/)说过用Sphinx给同事搭引擎，可是那是建立在之前的配置文件之上，我只要依葫芦画瓢，改一改路径以及查询语句就搞定了，实质上没学到什么东西。在我看来，要想真正了解它，还是得重新造轮子，从头到尾自己搭一遍，在这个过程中出现了许多奇怪的错误，在这里记录一下。

1.checking for clock_gettime in -lrt...
这是我遇到的第一个问题，事实证明，这根本不是问题。到Sphinx-for-chinese下载了编译包，开始编译，之后就卡在了这里。刚开始以为是缺少librt，然而我在lib中找到了这个链接库。将编译包放在其它机器上编译，又是可以通过的，百思不得其解。只好到Sphinx-fro-chinese的QQ群里发问，黑猫给出解答是要将librt所在路径加入到etc/ld.so.conf，并运行ldconfig命令。按照他的办法，结果运行ldconfig命令时卡住了，于是可以断定是机器的问题。

2.ERROR: cannot find MySQL include files.
这个问题比较好解决，就是缺少MySQL的库文件。因为虚拟机装的是Ubuntu，只要运行以下命令就好了。
sudo apt-get install libmysql++-dev libmysqlclient15-dev checkinstall
如果是其它系统，相信也是类似的方法。如果已经有库文件了，则只需要将路径加入到/etc/ld.so.conf中，并执行ldconfig命令

3.index 'test1': search error: query too complex, not enough stack (thread_stack=1217498K or higher required).
这也是一个很奇怪的错误。我是按照文档中给出的例子建好索引，之后用命令行工具，也就是search要搜索的，结果就出现了这个错误。在网上搜索这个错误，没找到有用的信息，于是又求助于Sphinx-for-chinese群，群里的人说是因为命令行存在问题，用客户端搜就没问题。于是用客户端搜果然没问题，可是我还是无法释怀，因为之前公司的引擎中，用命令行是没有问题的。于是对照着公司用的引擎中的配置文件，发现配置文件中没有这一行，在自己的配置文件中注释掉这行后，果然没问题了。
所以对于这个错误的解决办法就是，将sql_query_info = SELECT * FROM documents WHERE id=$id这行注释掉.
这个确实太坑人了，连官方的配置文件都会出错，得浪费多少人的时间。

4.ERROR: index 'main': No fields in schema - will not index.
光运行例子是不行的，还是得自己写一些东西，于是将自己的博客文章来搜索。用了Wordpress中wp_posts表中的数据，我只用的四个字段ID,post_title,post_content,post_modified,将post_title,post_content定义成sql_attr_string,sql_attr_timestamp,结果就出现了这个错误。在网上找了，发现在官方bug报告中有提到这个问题
[http://sphinxsearch.com/bugs/view.php?id=1632](http://sphinxsearch.com/bugs/view.php?id=1632)
管理员说，引擎中需要一个全文索引字段，否则就没有东西需要索引了，这样它就不会建索引。管理员建议定义为sql_field_string,这样就会对这个字段既索引又保存内容。对于我的配置，我并不想保存post_content这个字段，所以不想将它定义为sql_field_string,那怎样才能让它只被所以呢？看过文档之后，才知道默认情况下，是会被索引。这也是为什么，在上面的帖子中，将sql_attr_string = text注释掉就可以建索引了。所以我只能说管理员也没有真正理解这个错误的原因，看来不能迷信权威啊。

5.FATAL: there must be 2 indexes to merge specified
这个是在测试Klist的时，出现的。文档中说，当合并两个索引时，使用--merge-klists就可以将两个索引的klist合并，于是我在合并时加上了这个参数。具体如下：
./indexer -c $conf ?--rotate --merge --merge-klists delta deltaTemp
运行时就出现这个错误，我纳闷了，明明官方文档中说加入这个参数是没问题的。到网上找资料，有人是用--merge-killlists这个参数，试过之后，同样报这个错误。无奈之际，将--merge-klist参数放到--rotate前面，
./indexer -c $conf --merge-klists --rotate --merge delta deltaTemp
奇迹出现了，这次没有报错。我只能说，这真是个坑。

_《I__ntroduction to Search with Sphinx》_写的还是非常不错的，毕竟是Sphinx的作者，表达能力和写作能力自然非同凡响，关于Sphinx的知识，许多都来自本书。等有时间了，可以将引擎的搭建过程写一写，应该可以帮助一些人。这次搭建过程，我学到了许多，虽然用的是开源的引擎，但真要从头到尾搭建一个引擎，并提供可靠的服务，并不是那么容易的，还是得多实践才行。
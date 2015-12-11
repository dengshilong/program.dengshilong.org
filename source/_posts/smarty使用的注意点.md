title: smarty使用的注意点
tags:
  - smarty
  - 换行
id: 727
categories:
  - PHP
date: 2014-05-15 22:09:11
---

因为不会写MVC，所以只好使用模版，而在PHP中，一般使用Smarty.以下是自己在使用过程中，遇到的一些问题，以及需要注意的地方。

1.一般评论都是通过一个textarea输入，在显示的时候需要将换行幅\n替换成标签,当尝试使用replace : '\n' : '
''时，一直不可行，后来才知道，原来有nl2br这个函数。

2.对于使用addslashes过滤的内容，则需要使用stripslashes将添加的\去掉。

3.对于left_delimiter和right_delimiter的选择，我的经验是{ {和}}比较好，对于<{和}>最好不用，否则会遇到很多问题。

4\. 使用判断语句如{ {if}} { {elseif}} { {else}} { {/if}}时，千万不能在{ {和关键字中留出空格，否则会出错。如写成{ { /if }} { { else }}这些都会出错.
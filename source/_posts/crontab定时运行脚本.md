title: crontab定时运行脚本
tags:
  - crontab
  - shell
id: 642
categories:
  - shell
date: 2014-03-25 13:14:43
---

<div>在Linux上经常需要定时运行某个脚本，这是crontab就派上用场了。对于如何使用crontab,一般google。事实上，我一直很好奇的是，网上那些人关于crontab的知识到底从哪里得来的，知道man crontab后我才知道，原来他们也是看的手册。</div>
man crontab后，没有关于如何编写crontab任务的说明，看到see also crontab(5)后,执行man 5 crontab,发现这里有说明如何编写crontab任务。这样以后就不需要遇到一个问题，就上网找，直接看手册就好了。

一般说来，都是仿照晚上的例子写，如这里[http://www.blogjava.net/xiaomage234/archive/2007/12/26/170490.html](http://www.blogjava.net/xiaomage234/archive/2007/12/26/170490.html)后来才发现，给出的例子中有一个坑。
<div>* */1 * * * /usr/local/apache/bin/apachectl restart</div>
<div>每小时重启apache</div>
这个例子中说每小时重启apache，试着写了之后，才发现每一分钟都会重启。仔细分析后才发现原因,因为第一列是分钟的位置,而使用*号，则代表0-59分钟，于是在一个小时里，0-59分钟都会重启apache,等到59分钟重启apache后，已经过了一小时，于是又回到0分钟，于是apache又重启了。

所以以后遇到位置的命令时，不要立马上网找，可以先看看手册的说明。或者找一个靠谱的网页看，后来才发现[http://www.centos.bz/2011/03/auto-run-task-crontab/](http://www.centos.bz/2011/03/auto-run-task-crontab/)这里写的比较靠谱。在找这些命令使用过程中发现，网上这般人经常抄来抄去的，浪费别人的时间，太无聊了。
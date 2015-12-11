title: 安装Maven
tags:
  - Maven
id: 621
categories:
  - 软件安装
date: 2014-03-08 12:10:01
---

很早之前，在写第一个Servlet时，一直配置不成功，写一个Hello World!都成问题，于是转而奔向PHP，最近由于工作需要，要重新拾起Java那套东西。因为是用Maven做的管理，于是要安装Maven，到网上找参考资料，竟没安装好，于是到官网找解答，最终找到。

安装Maven之前，已经假设你安装好JDK.有一点需要注意的是,Maven3.2要求JDK1.6及以上,Maven3.0/3.1则要求JDK1.5及以上，否则会出现版本错误

1.下载Maven

到官网http://maven.apache.org/下载Maven,当前最新稳定版本为3.2.1

对于Windows系统，下载Maven 3.2.1 (Binary zip)

2.解压Maven,配置环境变量

将Maven解压，这里假设放在d:\apache-maven-3.2.1

之后进行环境变量配置，

在系统变量中增加M2_HOME,值为d:\apache-maven-3.2.1

在系统变量中增加M2,值为%M2_HOME%\bin

如果已经存在用户变量Path，则在值的前面增加%M2%； 注意一定要加上这个分号

如果不存在用户变量Path,则新建它，并赋值为%M2%

3.测试Maven

在命令行中执行mvn --version，在我的电脑上显示如下,

Apache Maven 3.2.1 (ea8b2b07643dbb1b84b6d16e1f08391b666bc1e9; 2014-02-15T01:37:5

2+08:00)

Maven home: d:\apache-maven-3.2.1

Java version: 1.6.0_15, vendor: Sun Microsystems Inc.

Java home: D:\Java\jdk1.6.0\jre

Default locale: zh_CN, platform encoding: GBK

OS name: "windows 7", version: "6.1", arch: "x86", family: "windows"

如果不是这样，看看环境变量是否配置正确，以及JDK版本是否匹配

4.Eclipse的Maven插件安装

在插件安装上，网上的资料很多已经过时了，因为都是很早之前的链接。顺着官网找到了eclipse的Maven插件安装链接http://download.eclipse.org/technology/m2e/releases/

我用的是Eclipse Kepler.在Help->Install new software中，将以上安装链接加入，名字为Maven，之后即可下载插件

[![Maven插件安装](http://program.dengshilong.org/wp-content/uploads/2014/03/Maven插件安装.png)](http://program.dengshilong.org/wp-content/uploads/2014/03/Maven插件安装.png)

5.配置Maven插件

在Window->Preferences中,选择Maven

[![Maven-Installations配置](http://program.dengshilong.org/wp-content/uploads/2014/03/Maven-Installations配置.png)](http://program.dengshilong.org/wp-content/uploads/2014/03/Maven-Installations配置.png)

点击Installations,此时还是用插件自带的Maven版本3.0.4,而且Global settings是空的我们需要添加自己安装的版本，点击Add,打开D:\apache-maven-3.2.1即可，最终结果如下：

[![Maven-Installations配置结果](http://program.dengshilong.org/wp-content/uploads/2014/03/Maven-Installations配置结果.png)](http://program.dengshilong.org/wp-content/uploads/2014/03/Maven-Installations配置结果.png)

此时Maven插件将会使用安装的Maven3.2.1版本

之后点击User Settings,可以看到如下结果

这里也许最让你迷惑的是这三个概念，Global Settings, User Settings,以及Local Repository。因为我也未深入理解，所以也只能在这里说说我的理解。简单来说，

Global Settings就是一些全局设置，设置了中央jar仓库的位置等等.

User Settings设置了用户私有jar仓库的位置等等.

Local Repository是本地jar仓库的位置.

假设你现在在开发一个应用，它需要使用一个jar,则Maven会先到Local Repository中寻找，如果没找到这个jar,则它会到User Settings中设置的用户私有jar仓库中查找，如果还是没找到，则到Global Settings设置的中央jar仓库中查找，如果还是没找到，Maven将报错，指示jar未找到。

网上还有介绍另外一种方法，也就是先去下载Eclipse的Maven插件，之后再将插件导入到Eclipse, 只是因为直接用URL的方法已经解决了安装问题，所以没有尝试。

6.Hello World例子

之后用《Maven by Example》中的一个例子来介绍安装介绍。命令行进入Eclipse工作目录，我这里是d:\workspace,执行以下命令

mvn archetype:generate -DgroupId=org.sonatype.mavenbook -DartifactId=simple -Dpackage=org.sonatype.mavenbook -Dversion=1.0-SNAPSHOT

之后敲几次回车，一个最简单的HelloWorld项目就建立好了。

之后cd simple进入simple目录，如果你有兴趣，可以看看Maven生成的内容，

其目录结构如下

simple/

simple/pom.xml

simple/src/main

simple/src/main/java

simple/src/test

simple/src/test/java

其中src/main存放源文件,src/test存放测试文件,pom.xml为Maven提供编译信息，

执行mvn install，编译,测试，打包项目

执行java -cp target/simple-1.0-SNAPSHOT.jar org.sonatype.mavenbook.App

看到输出的 Hello World！

事实上，在命令行中，一个困惑是如何选择新建项目的类型，命令行里一共列出了九百多种，而很难知道哪个编号对应的是哪一种项目类型。

关于Maven的更多内容可以去sonatype官网下载《Maven by Example》,绝对值得一看。

参考文章：

http://www.blogjava.net/fancydeepin/archive/2012/07/13/eclipse_maven3_plugin.html
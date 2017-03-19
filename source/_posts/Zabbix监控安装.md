title: Zabbix监控安装
date: 2017-03-19 23:46:32
tags:
    - Zabbix
categories:
---
[Zabbix](http://www.zabbix.com/)作为一款老牌监控，在服务器规模还不是很大时很有用。

安装Zabbix有很多种方式，这里使用rpm方式安装。因为服务器是CentOS 32位的，所以选择下面的rpm包，相应的包可以在[阿里云](http://mirrors.aliyun.com/zabbix/zabbix/3.0/rhel/)上找到。rpm -ivh http://mirrors.aliyun.com/zabbix/zabbix/3.0/rhel/6/i386/zabbix-release-3.0-1.el6.noarch.rpm, 具体安装见参考资料。

## 参考资料
* [Zabbix官方文档](https://www.zabbix.com/documentation/3.0/manual/api/reference)
* [自动化监控Zabbix安装部署之Server端部署](http://www.jianshu.com/p/5a2cb82e243f)
* [自动化监控Zabbix安装部署之agent端部署](http://www.jianshu.com/p/688da06320e8)
* [Zabbix使用实践](http://naixwf.github.io/2015/05/18/zabbix-practice/)

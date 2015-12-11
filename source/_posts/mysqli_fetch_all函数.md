title: mysqli_fetch_all函数
tags:
  - mysqli
  - mysqli_fetch_all
  - mysqlnd
id: 681
categories:
  - PHP
date: 2014-04-13 21:15:45
---

许多情况下，都需要将mysql的查询结果转成一个数组，这个就可以遍历数组来显示，查询结果。在我的开发环境里，我使用mysqli_fetch_all函数,使用方法如下

``` php
$result = mysqli_query($con, $sql);
$posts =  mysqli_fetch_all($result, MYSQLI_ASSOC);
```

加上MYSQLI_ASSOC是为了使返回的是关联数组,之后就可以遍历$posts数组。当将这段代码放到线上环境时，发现没有结果，最后才知道原来是mysqli_fetch_all函数无法使用。 google之后才知道,mysqli_fetch_all这个函数只存在于mysqlnd中，也就是PHP的原生MySQL驱动中。原来链接MySQL存在两套驱动,一套是libmysql,一套是mysqlnd。本来mysqlnd是不存在的,后来因为mysql到了Oracle手上之后,驱动的认证就有些问题了,于是PHP开发组自己开发了一套mysql驱动。

可是在linux下，安装mysqli时还是默认使用libmysql，所以要么就得重新安装mysqli模块,使用mysqlnd驱动安装，或者自己来实现mysqli_fetch_all的功能。暂时先自己实现类似的功能。
``` php
$result = mysqli_query($con, $sql);
$posts = array();
while($row = mysqli_fetch_array($result)) {
    $posts[] = $row;
}
```


title: 在C++的sort排序中永远让比较函数对相等的值返回false
tags:
  - C++
  - coredump
  - sort
  - 比较函数
id: 640
categories:
  - 编程
date: 2014-03-24 21:16:05
---

很久之前，线上的程序跑着跑着，莫名其妙的就coredump了，找了很久都不知道原因。因为coredump的次数不是很多，有时好几天了也才dump了一次，所以也很难确定是在哪个地方出错了。通过版本回溯，慢慢缩小了出错的范围，可是我还是不知道在哪里出错了，直到今天晚上组长和我说了可能出错的地方，才知道原来有这么一个坑存在。
<div></div>
<div>他说使用sort排序时，比较函数编写时，如果两个值相等返回true可能会存在问题，于是我看了自己写的，两个值相等时，正是返回true.</div>
<div>int cmp(const int &a, const int &b) {</div>
<div>    return a >= b;</div>
<div>}</div>
<div>可是我还是看不出这里有什么错误，google之后找到了解答,在一篇文章里说到，当排序的个数超过16个时，且这些书数全部相等时，如果比较函数在两个值相等返回true时就会出错。这是因为sort行数的实现中，当超过16个数时，使用快速排序，而且假定一定存在两个数不相等。具体可参看[http://blog.sina.com.cn/s/blog_79d599dc01012m7l.html](http://blog.sina.com.cn/s/blog_79d599dc01012m7l.html)</div>
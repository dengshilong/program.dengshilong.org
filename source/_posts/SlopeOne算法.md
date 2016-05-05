title: SlopeOne算法
date: 2016-05-05 20:54:38
tags: 推荐系统
categories: 大数据
---
最近公司说要做智能推荐，于是想起了协同过滤，想到了Slope One算法，虽然以前看过这个算法，但没有记笔记，这次只好从头看起，好在Slope One比较容易。


在[Wiki](https://en.wikipedia.org/wiki/Slope_One)上看了介绍，印象中有人用Python写了一个非常简洁的版本，于是在网上找。在[这里](http://www.serpentine.com/blog/2006/12/12/collaborative-filtering-made-easy/)找到详细说明，在[这里](https://github.com/kek/slopeone/blob/master/slope_one.py)找到代码。

| u\v | i   | i |
| ----|:---:| -:|
| u1  | 3   | 2 |
| u2  | 4   | 2 |
| u3  | 5   | ? |

对于上表中,使用 Slope One算法来预测用户u3对j 的评分具体过程是这样的:首先计算项目i和j的偏差,即((3 – 2) + (4 – 2)) / 2 = 1.5,之后预测用户u3对j的评分就可以这样计算5 – 1.5 = 3.5。

之后自己写了一个[版本](https://github.com/dengshilong/recommender/blob/master/src/main/SlopeOne.py)。

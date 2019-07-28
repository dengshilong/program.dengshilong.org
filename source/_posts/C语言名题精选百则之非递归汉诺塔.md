title: C语言名题精选百则之非递归汉诺塔
date: 2019-07-28 20:54:55
tags:
    - C名题百则
categories:
---
汉诺塔(Towers of Hanoi)是一个在入门书籍中常见的例题或习题, 它是说: 有3根柱子, 1、2与3,在柱子1上串了从上到下编号是1, 2, …, m的圆片, 号码小的圆片包小. 问题是, 请写一个程序,把柱子1上的圆片搬到柱子3去。在搬的时候有3个要求:第一, 每次只能搬一个圆片; 第二, 要搬的圆片得从某个柱子取出, 并且放到另一根柱子上; 第三,任何时刻、任何柱子上的圆片, 从上到下都是从小到大排列。书上的解法都是递归的, 请写一个非递归且不用堆栈来仿真的程序.

说明: 如果用教科书中的解法, 那么递归是个非常好且效率非常高的技巧, 程序大致如程下

```
#coding: utf-8

def hanoi_tower(n):
    return _hanoi_tower(n, 1, 2, 3)


def _hanoi_tower(n, start, mid, end):
    if n == 1:
        print("Move disk %d from %d to %d" % (n, start, end))
    else:
        _hanoi_tower(n - 1, start, end, mid)
        print("Move disk %d from %d to %d" % (n, start, end))
        _hanoi_tower(n - 1, mid, start, end)


if __name__ == "__main__":
    hanoi_tower(3)
```

这个观点是, 先把在start柱子上的n-1个圆片搬到mid柱子上去(用end柱子作中继站), 于是在strt柱子上就留下3在最下方, 也就是最大的一个圆片, 即第n号, 把它从start搬到end去(见print); 现在的情况是, 最大的已经到了目的地, 但在上方的第1 ~ n－1号还停留在mid柱子上; 第三步就是把mid上的n-1个圆片搬到end柱子上, 用start柱作中继站。当然, start、mid、end就是题目中的3根柱子, n是要搬的圆片数目.

递归的解不但漂亮, 而且容易懂; 不过了解了递归解法之后产能够由它而发展出一个非递归的解吗? 当然, 用堆栈来仿真并不是所期望的, 应该把递归动作中在什么时候搬那个圆片, 从何处搬到何处这一层关系弄清楚, 那么问题就不难了。

参考文献: 河内之塔(Towers of Hanoi)是法国人 M. Claus( Lucas)在1883年从泰国带到法国的(越南那个时候是法国属地), 河内曾经是越战时北越的首都, 现在的胡志明市。有很多人译成“汉诺威塔”是不对的, 音虽相差不远, 但却显然地误解了Hanoi这个字。河内之塔有一个起源的故事, 这是De Parville在1884年讲的。在Benares地方有一座神庙,从天神创世起, 就在神庙地底、大地的中心处立了3根钻石的针, 一根针上串了64个用金子铸成的圆片,从上到下圆片愈来愈大,神庙的僧侣按照前面提过的方法把这64个金圆片搬到第三根钻石针上,一旦工作完成,这些针、圆片、神庙以及这个世界都会随之消失。这段时间有2-1长, 亦即18446744073709551615步,纵使僧侣毫不犯错,恐怕也得花几百亿年才能搬得完。以上的史料出自下面两本书:

1. W.W. Rouse Ball and H.S. M Coxeter. Mathematical Recreations and Essays. 13th ed, Dover, 1987
2. M. Kraitchik Mathematical Recreations. 2nd ed. Dover. 1953 不用递归法来解河内之塔,曾经是一个很热门的业余问题,文献相当多,本文不打算一列举,与Gay码的联系也陆续地被人们一再“发现”,本书方法是取自 H. Mayer(加州圣地亚哥州立大学教授)与 Don Perkins(美制四年级,等于中国的高一学生)在1985年的一篇文章, Mayer教授指出这是Perkins想出来的方法,但他们两位都不曾指出这个方法与Gray码的联系,不过 Perkins不知道Gray码是可以预见的
3. H Mayer and D. Perkins. Towers of Hanoi Revisited, A Nonrecursive Surprise, SIGPLAN Notices.Vol.19(1984),No.2,pp.80~84 这方面的中文文献并不多,前几年笔者在《Mcmo随笔》上一连写过3个月的介绍或许可以提供参考。那3篇文章入手比较浅,也不曾提到Gray码, 所以有些地方说得不很清楚,如果现在有机会重写, 一定可以做得更好。在那一系列的第三篇中, 还有另一个有的公式与进一步的参考文献, 有兴趣的朋友可以一看
4. 冼镜光.谈河内之塔《Micro随笔》,微电脑时代.1986年9月 pp.170~174; 1980年10月, pp156~163; 1986年11月, pp.159~163

解答见[hanoi_tower.py](https://github.com/dengshilong/C100Problem/blob/master/chapter8/hanoi_tower.py)

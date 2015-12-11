title: POJ2524-Ubiquitous Religions
tags:
  - 并查集
id: 857
categories:
  - 数据结构
date: 2014-08-13 12:21:09
---

连并查集都忘记是怎么回事了，实在是不应该。还是复习一下为妙。
poj2524这一题是并差集的简单应用，先从这题开始。

There are so many different religions in the world today that it is difficult to keep track of them all. You are interested in finding out how many different religions students in your university believe in.

You know that there are n students in your university (0 < n <= 50000). It is infeasible for you to ask every student their religious beliefs. Furthermore, many students are not comfortable expressing their beliefs. One way to avoid these problems is to ask m (0 <= m <= n(n-1)/2) pairs of students and ask them whether they believe in the same religion (e.g. they may know if they both attend the same church). From this data, you may not know what each person believes in, but you can get an idea of the upper bound of how many different religions can be possibly represented on campus. You may assume that each student subscribes to at most one religion.

input:
The input consists of a number of cases. Each case starts with a line specifying the integers n and m. The next m lines each consists of two integers i and j, specifying that students i and j believe in the same religion. The students are numbered 1 to n. The end of input is specified by a line in which n = m = 0.

output:
For each test case, print on a single line the case number (starting with 1) followed by the maximum number of different religions that the students in the university believe in.

sample input
10 9
1 2
1 3
1 4
1 5
1 6
1 7
1 8
1 9
1 10
10 4
2 3
4 5
4 8
5 8
0 0
sample output
Case 1: 1
Case 2: 7
题目描述
​世界上有许多不同的宗教，要记录全部是很困难的。你有兴趣找出在你所在的大学，有多少不同宗教信仰的学生。

你所在的大学有n个学生(0 < n <= 50000).问遍所有学生的宗教信仰是不实际的。并且，一些学生对于表达他们的信仰会觉得不舒服。一个避免这些问题的解决办法是问m(0 <= m <= n(n-1)/2)对学生，他们是否属于同一个宗教(也就是他们同时出现在相同的教堂).从这些数据里，你不能知道每一个人的信仰，但是可以知道校园里宗教数量的一个上界。你可以假设一个学生至多属于一个宗教。

输入：
输入中包含一些测试用例。每个例子由一行包含整数n和m开始。接下来的m行由两个整数i和j组成,i和j属于同一个宗教.学生从1到n编号.输入的结束由一行n = m = 0标示.

输出：
每一个测试用例，输出一个数字标示第几个测试用例(从1开始)跟着是这所大学的所有学生可能的最大宗教信仰数。

``` c
#include <stdio.h>
#include <iostream>
using namespace std;
const int MAX=50001;
int father[MAX];
int rank[MAX];
void make_set(int x) {
    father[x] = x;
    rank[x] = 1;
}
int find_set(int x) {
    if (x != father[x]) {
        father[x] = find_set(father[x]);
    }
    return father[x];
}
void union_set(int x, int y) {
    int fx = find_set(x);
    int fy = find_set(y);
    if (fx == fy)
        return;
    if (rank[fx] > rank[fy]) {
        father[fy] = fx;
        rank[fx] += rank[fy] ;
    } else {
        rank[fy] += rank[fx];
        father[fx] = fy;
    }
}
int main() {
    int n, m, a, b;
    int test_case = 0;
    while (true) {
        scanf("%d %d", &n, &m);
        if (n == 0 && m == 0) {
            break;
        }
        test_case++;
        for (int i = 1; i <= n; i++) {
            make_set(i);
        }
        while (m--) {
            scanf("%d %d", &a, &b);
            union_set(a, b);
        }
        int count = 0;
        for (int i = 1; i <= n; i++) {
            if (i == father[i]) {
                count++;
            }
        }
        printf("Case %d: %d\n", test_case, count);
    }
    return 0;
}
```
title: 产生Gray码
tags:
  - C名题百则
id: 1053
categories:
  - 算法
date: 2015-10-29 16:40:43
---

编写一个程序，用Gray码(Gray Code)的顺序列出一个集合的所有子集。

什么是Gray码? nbit的Gray码是一连串共有2的n次方个元素的数列，每一个元素都有nbit,而且任何相邻的两个元素之间都只有1bit的值不同。例如，
两个bit的Gray码:
00 01 11 10 是一组Gray码
3个bit的Gray码:
000 001 011 010 110 111 101 100 是一组Gray码
但是Gray码并不是惟一的，把他循环排列或是用反过来的顺序写，也会得到一组Gray码；比如说，如果把3bitGray码的最后3个元素放在前面去，就会得到:
111 101 100 000 001 011 010 110 也是一组Gray码

产生Gray码的方法很多，这里这介绍其中一种。
将2bit Gray码列出
00 
01
11
10
将3bit Gray码列出
000
001
011
010
110
111
101
100
观察3bit Gray码可以发现，它可以由2bit Gray码来得到。
3bit Gray码的前四个由2bit Gray码从第一个到最后一个在最前面的加上0得到
3bit Gray码的后四个 可以将2bit Gray从最后一个到第一个在最前面加上1得到
写成代码如下
``` 
public class GrayCode {
    public static List<Integer> grayCode(int n) {
         List<Integer> result = new ArrayList<Integer>();
         if (n == 0) {
             result.add(0);
         } else {
             List<Integer> temp = grayCode(n-1);
             for (Integer i: temp) {
                 result.add(i);
             }
             for (int i = temp.size() - 1; i >= 0; i--) {
                 result.add(temp.get(i) + (1 << (n - 1)));
             }
         }
         return result;
    }
    public static void main(String[] args) {
        List<Integer> result = grayCode(1);
        for (Integer i: result) {
            System.out.println(i);
        }
    }
}
```

title: 重温manufactoria
tags:
  - manufactoria
id: 855
categories:
  - 编程
date: 2014-08-13 10:26:17
---

最近又玩了一遍manufactoria,发现有些关卡都快忘记怎么过的，这次还是写下来好了。
关卡按照从左到右，从上到下计数。
1\. Move robots from the entrance(top) to the exit (bottom)! 将机器从入口(顶部)移到出口(底部)!
简单，不多说
2\.  If a robot's string starts with blue, accept. Otherwise, reject!  如果机器以蓝色字符开头，则接受。否则，丢弃。
3\.  ACCEPT:if there are three or more blues! 如果有三个或三个以上的蓝色的，则接受
4\. ACCEPT: if a robot contains NO red! 如果机器不包含红色的，则接受。
5\. OUTPUT:The input,but with the first symbol at the end!  对于输入的字符，将第一个字符移到末尾作为输出
6\. ACCEPT: if the tape has only alternating colors! 如果只存在交替字符，则接受。
意思就是字符如果是交替出现的则接受，如蓝红蓝红蓝，红蓝红蓝等等，而蓝蓝红，红蓝蓝等出现连续相同的字符，所以不接受
7\. OUTPUT：Replace blue with green, and red with yellow! 输出：将蓝色换成绿色，将红色换成黄色。
8\. ACCEPT: if the tape ends with two blues!  如果末尾是两个蓝色，则接受。
9\. OUTPUT： Put a green at the begining,  and a yellow at the end! 输出： 对于输入的字符，在开头中添加一个绿色字符，在末尾中添加一个黄色字符。
10\. ACCEPT: Strings that begin and end with the same color! 如果开始字符和结束字符时相同，则接受。
11\. ACCEPT: With blue as 1 and red as 0, accept odd binary string! 把蓝色当做1，红色当做0， 接受奇数二进制数。
其实就是接受蓝色结尾的字符。
12\. ACCEPT: Some number of blue, then the same number of red! 接受： 一些蓝色的，然后相同数量的红色的。
也就是接受诸如蓝蓝红红，蓝蓝蓝红红红等，当然空字符也要接受，因为空字符代表0个蓝色，0个红色。
解决办法是每次除去一个蓝色和红色
13.OUTPUT: Swap blue for red, and red for blue! 输出： 将蓝色换成红色，红色换成蓝色。
也就是将字符串中的颜色互换。
14\. OUTPUT: All of the blue, but none of the red! 输出字符串中的所有蓝色字符，不输出红色字符。
也就是将字符串中的所有红色字符去掉，留下蓝色的。
15\. OUTPUT： The input, but with the last symbol moved to the front! 输出： 对于输入的字符，将最后一个字符移动最前面。
在末尾添加一个绿色，用来标示最后一个字符
16\. OUTPUT: With blue as 1 and red as 0, multiply by 8! 输出：把蓝色当做1，红色当做0，将二进制字符串乘以8.
其实也就是在字符串末尾添加3个0，也就是添加三个红色
17.ACCEPT: With blue as 1 and red as 0, accept binary strings > 15! 接受：把蓝色当做1，红色当做0，接受大于15的字符串。
18\. An equal number of blue and red, in any order! 只要字符串中包含相同个数的蓝色和红色，则接受。
使用与12相同的办法
19.OUTPUT：Put a yellow in the middle of the (even-lenght) string! 输出： 在字符串（偶数个字符串）的中间放置一个黄色字符。
在头尾都添加黄色，之后每个循环，头部的向前移一步，尾部的向后移一步。
20.ACCEPT: X blue, then X red, then X more blue, for any X! 接受： X个蓝色，然后X个红色，接着X个蓝色，对于X没有限制。
也就是接受蓝红蓝，蓝蓝红红蓝蓝等字符串，对于空字符也接受，因为它代表0个蓝色，然后0个红色，接着0个蓝色。
使用与12题相同的办法
21.OUTPUT: The input, but with all blues moved to the front! 输出：对于输入，将字符串中所有的蓝色移到前面。
逆向思维，将红色字符移到后面
22.OUTPUT: With blue as 1 and red as 0, add 1 to the binary string! 输出： 将蓝色当做1，红色当做0，将二进制字符串加上1.
在末尾添加一个黄色，每个循环，如果黄色左边的是蓝色，则蓝色变成红色，并且黄色左后退一个字符，
如果黄色左边的红色，则将红色变成蓝色，程序结束。
23\. ACCEPT: With blue as 1 and red as 0,  accept natural powers of four! 接受：把蓝色当做1，红色当做0，接受四的开方
24.ACCEPT: (Even-length) strings that repeat midway through! 接受：(偶数长度)接受从中间开始重复的字符串
意思就是接受的字符串是偶数长度，前半段和后半段是一样的，如蓝红红蓝红红，
25\. ACCEPT: If there are exactly twice as many blues as red! 接受：如果蓝色的个数是红色个数的两倍，则接受。
每个循环，除去两个蓝色和一个红色
26\. OUTPUT: Reverse the input string! 输出：将输入的字符串逆转输出
27.OUTPUT: Subtract 1 from the binary string!(Input >= 1) 输出：从二进制字符串中减去1(输入字符串>=1)
在末尾添加一个黄色，每个循环，如果黄色左边的是红色，则红色变成蓝色，并且黄色左后退一个字符，
如果黄色左边的蓝色，则将蓝色变成红色，程序结束。
28.ACCEPT: Perfectly symmetrical strings! 接受：完美对称字符串！
意思就是回文串，也就是从左读到右和从右读到左是一样的。
每个循环，头尾消去的字符是一样的。
29.ACCEPT: Two identical strings, separated by a green! 接受：两个相同的字符串，由绿色隔开。
30\. ACCEPT: Read the tape as two numbers, A and B, split by a green: accept if A > B! 接受：读入的字符串当做两个二进制数，A和B，由一个绿色隔开，如果A>B则接受。
每次比较A和B的字符，分四种情况
蓝蓝，继续比较A和B剩余的字符
红红，继续比较A和B剩余的字符
蓝红，这种情况下，有个小技巧，将B的字符再消去一个，这时A剩余的字符比B剩余的字符长，则A>B
红蓝,A剩余的字符比B剩余的字符长，则A>B
31\. OUTPUT: Read the tape as two numbers, A and B, split by a green: output A + B! 输出：读入的字符串当做两个二进制数，A和B，由一个绿色隔开，输出A+B的和！
将A和B都转成黄色字符，之后再将黄色字符转成二进制。
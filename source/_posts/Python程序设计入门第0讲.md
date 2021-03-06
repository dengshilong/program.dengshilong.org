title: Python程序设计入门第0讲
date: 2019-06-30 16:31:37
tags:
    - Python
categories:
---
前些天，有个姑娘说想学Python，我一听，双眼放出万丈光芒，心想如果我教会她，万一姑娘一时高兴，以身相许，老妈就再也不用担心我了，那岂不是美滋滋。于是准备要怎么教她学编程，夜晚，躺在床上，回忆自己的编程经历，想起高一时与朝辉一起学习VBasic的点点滴滴，想起大一时为了考C语言二级的突击学习，真是岁月如梭。一顿感慨后，心中已有了大致的想法，于是有了这篇文章。

几乎所有的编程语言，都是由3种基本的程序结构组成，顺序，循环，选择，弄懂这三种后，就可以写程序了。下面且听我一一道来。

### print
先来看看print语句

```
print('邓世龙')
输出 邓世龙
```

```
a = 1
b = 2
print(a, b)
输出 1 2
```

### 顺序结构
然后来看顺序结构, 顺序结构很容易理解，就是程序是一句句往下执行，

```
a = 1
b = 2
a = 3
b = 4
print(a, b)
输出 3 4
```

```
s = 0
print(s)
s = s + 1
print(s)
s = s + 2
print(s)
s = s + 3
print(s)
s = s + 4
print(s)

输出如下
0
1
3
6
10
```

接下来看看循环结构。现在我们要完成一个计算任务，计算1 + 2 + 3 + ... + 10的和，我们可以从1一直加到10，这就需要循环。在绝大多数编程语言里，都提供for或者while来完成循环，这里先来看for, 而在这之前，先了解下list, 也就是列表。

### list(列表)
list相当于其它编程语言里的数据，主要是用来存放统一类型的数据

```
x = [1, 2, 3, 4, 5, 6]
print(type(x))  # 显示x的类型
print(len(x))   # 求列表的长度
print(x[0])     # 取第一个值
print(x[2])     # 取第三个值
print(dir(x))   # 显示列表的变量和方法

输出如下
<class 'list'>
6
1
3
['__add__', '__class__', '__contains__', '__delattr__', '__delitem__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__iadd__', '__imul__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__rmul__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', 'append', 'clear', 'copy', 'count', 'extend', 'index', 'insert', 'pop', 'remove', 'reverse', 'sort']
```

### range

1到6的列表手写问题也不大，但1到100，1到1000的列表如果手写会疯掉的，所以Python提供了range这个函数。

```
x = list(range(10))
print(x)
y = list(range(1, 10))
print(y)
z = list(range(1, 10, 2))
print(z)

输出如下
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
[1, 2, 3, 4, 5, 6, 7, 8, 9]
[1, 3, 5, 7, 9]
```

### 循环结构 for 

下面就是for循环的语法，注意for循环后面有冒号，之后print还要缩进

```
# for循环 打印1到10
n = 10
for i in range(1, n + 1):
    print(i)
    
输出如下:
1
2
3
4
5
6
7
8
9
10  
```

现在我们就可以编写求1 + 2 + 3 ... + 10的和的程序

```
# 循环，for循环求和, 求1 + 2 + ... + 10的和, 

s = 0
n = 10
for i in range(1, n + 1):
    s = s + i
print(s)

输出
55
```

### 选择 if
现在我们要求1到10以内，所有偶数的和，这就会用到选择。

那么如何判断是偶数呢？对2取余就行了，如果余数是0，就是偶数

```
print(4 % 2 == 0)  # % 是求余操作
print(3 % 2 == 0)
输出
True
False
```
现在加上if判断，求1到10以内所有偶数的和

```
s = 0
n = 10
for i in range(1, n + 1):
    if i % 2 == 0:
        s = s + i
print(s)
```

#### 选择 and
如果要求30以内，既能被3，又能被5整数的所有整数的和，这时候就会用到and操作

```
s = 0
n = 30
for i in range(1, n + 1):
    if i % 3 == 0 and i % 5 == 0:  # 有15，30
        s = s + i
print(s)
输出
45
```

#### 选择 or
如果要求10以内，能被3，或能被5整数的所有整数的和, 这时候就会用到or操作

```
s = 0
n = 10
for i in range(1, n + 1):
    if i % 3 == 0 or i % 5 == 0:  # 有 3，5，6，9，10
        s = s + i
print(s)
```

#### continue 进入下一次循环
求10以内，能被3或能被5整数, 但不能被2整除的所有整数的和，这时候可以继续使用and和or的组合来判断，但更方便的，还是用continue,

```
s = 0
n = 10
for i in range(1, n + 1):
    if i % 2 == 0:
        continue
    if i % 3 == 0 or i % 5 == 0:  # 有 3，5，9
        s = s + i
print(s)
输出
17
```

### 循环 while
for循环也可以用while循环来代替, while后面跟着判断条件，如果条件为True, 也就是为真，就会一直执行while循环里的内容; 如果为False，就会跳出循环。例如求1 + 2 + ... + 10的和，用for循环编写如下

```
s = 0
n = 10
for i in range(1, n + 1):
    s = s + i
print(s)
```
改成while，如下
```
s = 0
i = 1
n = 10
while i <= n:
    s = s + i
    i = i + 1
print(s)
```

既然有了for循环, 为何还要有while循环呢？考虑这样一个问题，求前6个能被3或5整除的整数的和。这时如果用for循环，就不是很合适，因为你不知到要到什么时候才能结束, 这种情况用while循环就很方便。

```
s = 0
i = 1
count = 0
n = 6
while count < n:
    if i % 3 == 0 or i % 5 == 0: # 前6个为 3，5，6，9，10, 12
        s = s + i
        count = count + 1
    i += 1
print(s)
输出
45
```

也就是说for循环主要用于确定循环次数的场合，而while循环主要用途循环次数不定的场合

#### 循环 break
break用于跳出循环，上面的例子也可以修改为如下程序

```
s = 0
i = 1
count = 0
n = 6
while True:
    if i % 3 == 0 or i % 5 == 0: # 前6个为 3，5，6，9，10, 12
        s = s + i
        count = count + 1
        if count == n:
            break
    i += 1
print(s)
```

下面再讲讲set, dict还有函数，就可以编写实际代码了。

### set 
set就是集合，主要用来提高查询速度

```
s = list(range(1, 100000000))
x = set(s)
print('#')
print(99999999 in s)
print('##')
print(99999999 in x)
```

在上面的例子中99999999 in s这里会有些卡顿，因为它要从s里的第一个数从前往后一个一个比较，而99999999 in x这里执行非常快，因为set是优化过的数据结构，底层实现是哈希表，可以很快的进行查询

### dict
dict，也就是字典，和set类似，只不过多了个value值，也用来提高查询速度，应用广泛，例如查询身份证号对应的一些个人用户信息等等

```
d = {'a': 65, 'b': 66}
print(d['a'])
输出
65
```

### 函数

函数就是一些可以重复利用的代码段。例如要求1到10的所有整数的和，与求2到5所有整数的和，这是两个类似的问题，就可以编写求和函数来解决，求和函数如下。声明一个函数是用def关键字，然后是函数名，后面跟着参数。

```
def my_sum(a, b):
    s = 0
    for i in range(a, b + 1):
        s = s + i
    return s

print(my_sum(1, 10))
print(my_sum(2, 5))
输出
55
14
```

到了这里，三种程序结构就讲完了，弄懂这三种结构就可以编写更大一些的程序，解决实际问题。而实际上，绝大多数程序，都是由这三种基本结构构成的，无非就是更复杂的数据结构和算法，还有调用库函数。

最后问题来了，我在哪里输入这些代码呢？Jupyter notebook了解下。

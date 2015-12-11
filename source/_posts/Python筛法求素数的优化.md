title: Python筛法求素数的优化
tags:
  - 列表解析
  - 筛法
  - 素数
id: 882
categories:
  - 算法
date: 2014-08-16 21:13:21
---

在pythontip上做题时,有这样一道题，
给你一个正整数N(1 <= N <= 10000000)，求{1,2,3,...,N}中质数的个数。
如N=3， 输出2.
也就是求N以内质数的个数。
刚开始用以前写的筛法写了一个最初版本，
``` python
N = 10000000
primes = [True for i in xrange(N + 1)] 
primes[0] = primes[1] = False
for i in xrange(2, N + 1): 
    if not primes[i]:
        continue
    n = i * i 
    while n < N + 1:
        primes[n] = False
        n += i
print len([i for i in xrange(N + 1) if primes[i]])
```
发现超时，用time模块的clock测试,用了16s.之后一步一步优化，先将len([i for i in xrange(N + 1) if primes[i]])这句改成primes.count(True)时间缩短到14s,之后看了讨论组里的讨论,将
``` python
n = i * i 
    while n < N + 1:
        primes[n] = False
        n += i
```
这部分改成
``` python
primes[i * i:N + 1:i] = [False] * ((N - i * i) / i + 1)
```
时间没有明显的变化，因为看到[False] * ((N - i * i) / i + 1)，于是将[True for i in xrange(N + 1)] 这行改成[True] * (N + 1) ，速度明显加快，只用了4s,经过这样优化后，程序变成了
``` python
N = 10000000
primes = [True] * (N + 1) 
primes[0] = primes[1] = False
for i in xrange(2, N + 1): 
    if not primes[i]:
        continue
    primes[i * i:N + 1:i] = [False] * ((N - i * i) / i + 1)
print primes.count(True)
```
之后想办法将for循环去掉。于是将它改成
``` python
i = 2
while i * i <= N:
    if primes[i]:
        primes[i * i:N + 1:i] = [False] * ((N - i * i) / i + 1)
    i += 1
```
最终为
``` python
N = 10000000
primes = [True] * (N + 1) 
primes[0] = primes[1] = False
i = 2
while i * i <= N:
    if primes[i]:
        primes[i * i:N + 1:i] = [False] * ((N - i * i) / i + 1)
    i += 1
print primes.count(True)
```
时间跑到了2s以内，提交后通过了。

之后将之前求素数的程序[筛法得到素数](http://program.dengshilong.org/2014/07/15/%E7%AD%9B%E6%B3%95%E5%BE%97%E5%88%B0%E7%B4%A0%E6%95%B0/)进行修改,得到
``` python
def getPrimes(n):
    primes = [True] * (n + 1)
    primes[0] = primes[1] = False
    i = 2
    while i * i <= n:
        if primes[i]:
            primes[i * i:n + 1:i] = [False] * ((n - i * i) / i + 1)
        i += 1
    return [i for i in xrange(n + 1) if primes[i]]
```
​

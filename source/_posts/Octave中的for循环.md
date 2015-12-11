title: Octave中的for循环
tags:
  - octave
id: 844
categories:
  - 机器学习
date: 2014-07-20 10:56:32
---

之前就选修过Angrew Ng的机器学习,但是那是一味的只追求进度，所以收获甚微，于是这次又重新选修了这门课。

这么课程使用Octave语言，这可以说是Matlab的开源版本，使用这种高阶语言，可以让我们更专注于算法层面。今天在实现sigmoid函数时，老是出错。原来是忘记了在每个for循环之后加上end. 还有一点需要说明的是,在Octave中，数组是从1开始的。
[matlab]
x = [1 2; 3 4]
g = zeros(size(x));
for i = 1:size(x,1)
    for j = 1:size(x,2)
        g(i,j) = 1 / (1 + e ^ (-x(i, j)));
    end 
end
g
[/matlab]
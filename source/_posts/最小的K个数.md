title: 最小的K个数
tags:
  - 堆
  - 最小的K个数
id: 865
categories:
  - 数据结构
  - 算法
date: 2014-08-14 12:37:31
---

对于求最大的K个数和最小的K个数，一个解决的办法是使用堆，这里以最小的K个数为例。
题目描述：
输入n个整数，找出其中最小的K个数。例如输入4,5,1,6,2,7,3,8这8个数字，则最小的4个数字是1,2,3,4,。

输入：
每个测试案例包括2行：
第一行为2个整数n，k(1<=n，k<=200000)，表示数组的长度。
第二行包含n个整数，表示这n个数，数组中的数的范围是[0,1000 000 000]。

输出：
对应每个测试案例，输出最小的k个数，并按从小到大顺序打印。

样例输入：
8 4
4 5 1 6 2 7 3 8
样例输出：
1 2 3 4

对于这题，可以使用堆来解决。首先建立一个K个元素的大顶堆，对于之后的n-k个元素，每个与堆顶比较，如果大于堆顶，则它不可能是最小的K个数之一，如果小于堆顶，则将堆顶替换，并重建大顶堆。之后剩下的K个元素就是最小的K个数。对它们从小到大排序就可以得到结果。
写成代码如下：
``` c
#include <stdio.h>
#include <stdlib.h>
void swap(int &a, int &b) {
    int temp = a;
    a = b;
    b = temp;
}
void adjust_heap(int *a, int cur, int n) {
    int left, right;
    while (true) {
        left = 2 * cur + 1;
        right = 2 * cur + 2;
        int index = cur;
        if (left < n && a[left] > a[index]) {
            index = left;
        }
        if (right < n && a[right] > a[index]) {
            index = right;
        }
        if (index != cur) {
            swap(a[cur], a[index]);
            cur = index;
        } else {
            break;
        }
    }
}
void build_heap(int *a, int n) {
    for (int i = (n - 1) / 2; i >= 0; i--) {
        adjust_heap(a, i, n);
    }
}
void heap_sort(int *a, int n) {
    build_heap(a, n);
    for (int i = n - 1; i > 0; i--) {
        swap(a[0], a[i]);
        adjust_heap(a, 0, i);
    }
} 
int main() {
    int n, k, num;
    while(scanf("%d %d", &n, &k) != EOF) {
        int *a = new int[k];
        for (int i = 0; i < n; i++) {
            scanf("%d", &num);
            if (i <= k - 1) {
                a[i] = num;
                if (i == k - 1) {
                    build_heap(a, k);
                }
            } else {
                if (a[0] > num) {
                    swap(a[0], num);
                    adjust_heap(a, 0, k);
                }
            }
        }
        heap_sort(a, k);
        for (int i = 0; i < k - 1; i++) {
            printf("%d ", a[i]);
        }
        printf("%d\n", a[k - 1]);
        delete[] a;
    }
    return 0;
}
```
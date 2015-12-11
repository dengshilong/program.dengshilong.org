title: HDU2222-Keywords Search
tags:
  - AC自动机
id: 873
categories:
  - 数据结构
  - 算法
date: 2014-08-16 11:12:23
---

AC自动机作为多模式匹配的经典方法，在关键词过滤中有重要应用，在我看来，AC自动机主要是这样几个步骤，第一步是先建立关键词的trie数，第二步是构建自动机，建立关键词之间的联系，第三步是利用第二步构建的自动机进行检索。HDU2222-关键词搜索是AC自动机的一个简单应用。关于AC自动机的资料，可以看这里[http://www.notonlysuccess.com/index.php/aho-corasick-automaton/](http://www.notonlysuccess.com/index.php/aho-corasick-automaton/).
**问题描述**
现在，搜索引擎如谷歌，百度等已经走进每个人的生活。
Wiskey也想在他的图片检索系统中实现这个功能。
每一张图片有一段描述，当用户输入关键字查找图片时，系统会将这些关键字与图片的描述进行匹配，然后显示与这些关键字最匹配的图片。
为了简化用题，这里给你出一段图片的描述，和一些关键字，请你告诉我​将匹配多少个关键字。
**输入**
第一行是一个整数，它的意思是有多少个测试用例。
每一个测试用例包含整数N，它的意思是有多少个关键字。(N <= 10000)
每一个关键字是由'a'-'z'的字符组成，长度不超过50.
用例的最后一行​是描述，长度不超过1000000.
**示例输入**
1
5
she
he
say
shr
her
yasherhs
**示例输出**
3

解法：
AC自动机的简单应用。有一个坑是，输入中关键词存在重复时，要计算多次。

代码如下
``` c
#include <iostream>
#include <stdio.h>
#include <string.h>
#include <queue>
using namespace std;
const int NUM = 26;
struct NODE {
    int cnt;
    NODE *fail;
    NODE *next[NUM];
    NODE () {
        cnt = 0;
        fail = NULL;
        memset(next, 0, sizeof(next));
    }
};

void insert(NODE *root, char *s) {
    NODE *cur = root;
    while (*s) {
        int index = *s - 'a';
        if (!cur->next[index]) {
            cur->next[index] = new NODE();
        }
        cur = cur->next[index];
        s++;
    }
    cur->cnt++;
} 
void ac_build(NODE *root) {
    queue <NODE *> q;
    NODE *cur;
    root->fail = NULL;
    for (int i = 0; i < NUM; i++) {
        if (root->next[i]) {
            root->next[i]->fail = root;
            q.push(root->next[i]);
        }
    } 
    while (!q.empty()) {
        cur = q.front();
        q.pop();
        for (int i = 0; i < NUM; i++) {
            if (cur->next[i]) {
                q.push(cur->next[i]);
                NODE *temp = cur->fail;
                while (temp) {
                    if (temp->next[i]) {
                        cur->next[i]->fail = temp->next[i];
                        break;
                    }
                    temp = temp->fail;
                }
                if (temp == NULL) {
                    cur->next[i]->fail = root;
                }
            }
        }
    }
}
int ac_find(NODE *root, char *s) {
    int sum = 0;
    NODE *cur = root;
    while (*s) {
        int index = *s - 'a';
        while (cur->next[index] == NULL && cur != root) {
            cur = cur->fail;
        }
        cur = (cur->next[index] == NULL) ? root : cur->next[index]; 
        NODE *temp = cur;
        while (temp != root && temp->cnt != -1) {  
            sum += temp->cnt;
            temp->cnt = -1;
            temp = temp->fail;
        }
        s++;
    }
    return sum;
}
int main() {
    int ncase, n;
    char word[51];
    char desc[1000001];
    scanf("%d", &ncase);
    while (ncase--) {
        NODE *root = new NODE();
        scanf("%d", &n);
        for (int i = 0; i < n; i++) {
            scanf("%s", word);
            insert(root, word);
        }
        scanf("%s", desc);
        ac_build(root);
        int res = ac_find(root, desc);
        printf("%d\n", res);
    }
    return 0;
}
```
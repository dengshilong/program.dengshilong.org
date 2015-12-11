title: POJ2001-Shortest Prefixes
tags:
  - trie
  - 前缀树
  - 字典树
id: 868
categories:
  - 数据结构
date: 2014-08-14 16:49:30
---

Trie又称为前缀树或字典树，它有许多重要用途，如搜索提示，以及作为AC自动机的基础。POJ2001-最短前缀这题是Trie的基础应用。
**Description**
A prefix of a string is a substring starting at the beginning of the given string. The prefixes of "carbon" are: "c", "ca", "car", "carb", "carbo", and "carbon". Note that the empty string is not considered a prefix in this problem, but every non-empty string is considered to be a prefix of itself. In everyday language, we tend to abbreviate words by prefixes. For example, "carbohydrate" is commonly abbreviated by "carb". In this problem, given a set of words, you will find for each word the shortest prefix that uniquely identifies the word it represents.

In the sample input below, "carbohydrate" can be abbreviated to "carboh", but it cannot be abbreviated to "carbo" (or anything shorter) because there are other words in the list that begin with "carbo".

An exact match will override a prefix match. For example, the prefix "car" matches the given word "car" exactly. Therefore, it is understood without ambiguity that "car" is an abbreviation for "car" , not for "carriage" or any of the other words in the list that begins with "car".
**Input**
The input contains at least two, but no more than 1000 lines. Each line contains one word consisting of 1 to 20 lower case letters.
**Output**
The output contains the same number of lines as the input. Each line of the output contains the word from the corresponding line of the input, followed by one blank space, and the shortest prefix that uniquely (without ambiguity) identifies this word.
**Sample Input**
carbohydrate
cart
carburetor
caramel
caribou
carbonic
cartilage
carbon
carriage
carton
car
carbonate
**Sample Output**
carbohydrate carboh
cart cart
carburetor carbu
caramel cara
caribou cari
carbonic carboni
cartilage carti
carbon carbon
carriage carr
carton carto
car car
carbonate carbona
​​​​​**描述**
一个字符串的前缀是从头开始的字符串的子串。"carbon"的前缀有："c","ca","car","carb","carbo"和"carbon".注意在这个问题中空串不认为是前缀，但是每个非空字符串自身可以认为是一个前缀。在日常用于中，我们倾向于用前缀来缩写词。例如，“carbohydrate"常缩写成"carb".在这个问题中，我们给出一系列单词，要求能够唯一标识单词的最短前缀。

例如在下面的例子中，"carbohydrate"可以缩写成"carboh",但是它不能缩写成"carbo"(或者更短),因为在这些词中，还有一个词是由"carbo"开始的.

精确匹配将覆盖前缀匹配。例如，前缀"car"精确匹配单词"car".因此,”car"可以毫无歧义的认为是"car"的简写,而不是"carriage"的，或者其它一些由"car"作为前缀的单词.
**输入：**
输入至少包含两个，不超过1000行，每行宝行一个由1到20个字母组成的单词。
**输出：**
输出包含与输入相同的行数。每一行输出由对应的输入组成，跟着一个空格，之后是唯一(无歧义)标示单词的最短前缀.
**示例输入：**
carbohydrate
cart
carburetor
caramel
caribou
carbonic
cartilage
carbon
carriage
carton
car
carbonate
**示例输出：**
carbohydrate carboh
cart cart
carburetor carbu
caramel cara
caribou cari
carbonic carboni
cartilage carti
carbon carbon
carriage carr
carton carto
car car
carbonate carbona
解答：
在节点中增加一个time字段来记录路径被经过的次数，如果time=1,则只出现一次，说明可以用来标示单词，作为最短前缀。
代码如下：

``` c
#include
#include
#include
using namespace std;
const int NUM = 26;
const int MAX = 1000;
const int LENGTH = 21;
char words[MAX][LENGTH];
struct NODE {
    int time;
    NODE *next[NUM];
    NODE () {
        time = 0;
        memset(next, 0, sizeof(next));
    }
};

void insert(NODE *root, char *s) {
    NODE *cur = root;
    while (*s != '\0') {
        int index = *s - 'a';
        if (!cur->next[index]) {
            cur->next[index] = new NODE();
            cur = cur->next[index];
            cur->time = 1;
        } else {
            cur = cur->next[index];
            (cur->time)++;
        }
        s++;
    }
}
void search(NODE *root, char *s) {
    NODE *cur = root;
    while (*s != '\0') {
        int index = *s - 'a';
        cur = cur->next[index];
        if (cur->time != 1) {
            printf("%c", *s);
            s++;
        } else {
            printf("%c", *s);
            break;
        }
    }
    printf("\n");
}
int main() {
    int total = 0;
    NODE * root = new NODE();
    while (scanf("%s", words[total]) != EOF) {
        insert(root, words[total]);
        total++;
    }
    for (int i = 0; i < total; i++) {
        printf("%s ", words[i]);
        search(root, words[i]);
    }
    return 0;
}
```
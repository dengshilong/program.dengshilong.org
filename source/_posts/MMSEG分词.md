title: MMSEG分词
tags:
  - mmseg
  - Python
  - 分词
id: 786
categories:
  - 搜索引擎
date: 2014-07-08 23:44:38
---

很早之前就知道MMSEG分词算法，网上也有各种语言的实现。最近了解Sphinx-for-Chinese的分词后，才知道它也是使用的MMSEG，并且CoreSeek也是使用的MMSEG。也许MMSEG是互联网上使用知名度最高的分词算法了吧，因为它简单并且高效。

更进一步了解后，知道MMSEG是台湾人蔡志浩提出来的。蔡志浩是一位心理学教师，在美国伊利诺伊读博士期间，选修了语言学，在这个过程中，随手写了MMSEG。看蔡志浩网站，总是很舒心，因为蔡老师的文笔很好，总会用通俗的语言把问题讲清楚，而且蔡老师的博客涉及范围极广，设计，心理，写作，社会观察，旅游等等。也正是因为他的博客，我才用实名建立自己的博客。以下回归正题。

MMSEG总的说来就是四个规则。
1.最长匹配原则
2.最大平均长度
3.最小长度方差
4.最大单字单词的语素自由度

算法步骤：
1.选定一个分词个数，得到可行的分词情形
2.利用4条原则得到最优分词可能
3.得到最优分词的第一个词，回到步骤1继续分词

举个例子最好理解。下面是要对“研究生命起源的原因主要是因为它的重要性”进行分词。
1.首先选定分词个数为3，则可以得到可行的分词情形如下：
研 究 生
研 究 生命
研究 生命 起
研究 生命 起源
研究生 命 起
研究生 命 起源
2.利用4条原则得到最优分词可能
运用第1条原则后，可以得到最优分词可能为一下两条
研究 生命 起源
研究生 命 起源
运用第2条原则，这两个结果相同
运用第3条原则，可以得到最优的结果为
研究 生命 起源
3.从最优结果中得到第一个词，也就是“研究”，之后对“生命起源的原因主要是因为它的重要性”运用相同的步骤进行分词

有必要对原则4进行解释，这条原则说的是单字的成为语素的自由度。当分到”主要是因为“就会用到。对于”主要是因为“
第1步骤中得到：
主 要 是
主 要是 因为
主要 是 因
主要 是 因为
第2步骤中，由前三条原则，只剩下一下两个
主要 是 因为
主 要是 因为
之后再运用第4条原则，这里单字”是“为独立语素的可能比”主“要大，所以最优结果为
主要 是 因为

见过的MMSEG算法实现中，素心如何天上月的[http://yongsun.me/2013/06/simple-implementation-of-mmseg-with-python/](http://yongsun.me/2013/06/simple-implementation-of-mmseg-with-python/)无疑是最简明清晰的。Python确实不错，短短100行就把算法的精髓展示出来，并且几乎可以不用写注释了。模仿他的实现，写了一遍。

``` python
#coding:utf-8
from collections import defaultdict
import codecs
from math import log

class Trie(object):
    class TrieNode():
        def __init__(self):
            self.value = 0
            self.trans = {}
    def __init__(self):
        self.root = self.TrieNode()
    def add(self, word, value=1):
        cur = self.root
        for ch in word:
            try:
                cur = cur.trans[ch]
            except:
                cur.trans[ch] = self.TrieNode()
                cur = cur.trans[ch]
        cur.value = value
    def _walk(self, node, ch):
        if ch in node.trans:
            node = node.trans[ch]
            return node, node.value
        else:
            return None, 0
    def match_all(self, s):
        ret = []
        cur = self.root
        for ch in s:
            cur, value = self._walk(cur, ch)
            if not cur:
                break
            if value:
                ret.append(value)
        return ret

class Dict(Trie):
    def __init__(self, filename):
        super(Dict, self).__init__()
        self.load(filename)

    def load(self, filename):
        with codecs.open(filename, "r", "utf-8") as f:
            for line in f:
                word = line.strip()
                self.add(word, word)
class CharFreq(defaultdict):
    def __init__(self, filename):
        super(CharFreq, self).__init__(lambda: 1)
        self.load(filename)
    def load(self, filename):
        with codecs.open(filename, "r", "utf-8") as f:
            for line in f:
                line = line.strip()
                word, freq = line.split(' ')
                self[word] = freq
class MMSEG():
    class Chunk():
        def __init__(self, words, chars):
            self.words = words
            self.lens = map(lambda x: len(x), words)
            self.length = sum(self.lens)
            self.average = self.length * 1.0 / len(words)
            self.variance = sum(map(lambda x: (x - self.average) ** 2, self.lens)) / len(words)
            self.free = sum(log(float(chars[w])) for w in self.words if len(w) == 1)
        def __lt__(self, other):
            return (self.length, self.average, -self.variance, self.free) < (other.length, other.average, -other.variance, other.free)
    def __init__(self, dic, chars):
        self.dic = dic
        self.chars = chars
    def __get_chunks(self, s, depth=3):
        ret = []
        def __get_chunk(self, s, num, seg):
            if not num or not s:
                if seg:
                    ret.append(self.Chunk(seg, self.chars))
                return
            else:
                m = self.dic.match_all(s)
                if not m:
                    __get_chunk(self, s[1:], num - 1, seg + [s[0]])
                else:
                    for w in m:
                        __get_chunk(self, s[len(w):], num - 1, seg + [w])
        __get_chunk(self, s, depth, [])
        return ret
    def segment(self, s):
        while s:
            chunks = self.__get_chunks(s)
            best = max(chunks)
            yield best.words[0]
            s = s[len(best.words[0]):]

if __name__ == "__main__":
    dic = Dict("dict.txt")
    chars = CharFreq('chars.txt')
    mmseg = MMSEG(dic, chars)
    print ' '.join(mmseg.segment(u"北京欢迎你"))
    print ' '.join(mmseg.segment(u"研究生命起源的原因主要是因为它的重要性"))
    print ' '.join(mmseg.segment(u'开发票'))
    print ' '.join(mmseg.segment(u'武松杀嫂雕塑是艺术，还是恶俗？大家怎么看的？'))
    print ' '.join(mmseg.segment(u'陈明真做客《麻辣天后宫》的那期视频哪里有？'))
    print ' '.join(mmseg.segment(u'压缩技术是解决网络传输负担的 有效技术。数据压缩有无损压缩和有损压缩两种。在搜索引擎中用到的压缩技术属于无损压缩。接下来，我们将先讲解各种倒排索引压缩算法，然后来分析搜索引擎技术中词典和倒排表的压缩。'))
```
用到的两个文件[dict.txt](http://program.dengshilong.org/wp-content/uploads/2014/07/dict.txt)和[chars.txt](http://program.dengshilong.org/wp-content/uploads/2014/07/chars.txt)

title: Sphinx-for-Chinese的分词细粒度问题
tags:
  - mmseg
  - Sphinx-for-chinese
  - 分词
  - 粒度
id: 769
categories:
  - 搜索引擎
date: 2014-06-28 22:31:51
---

假如使用Sphinx来做搜索引擎，就一定会遇到分词问题。对于中文，有两个选择，选择1是使用Sphinx自带的一元分词，选择2是使用CoreSeek或者Sphinx-for-Chinese，这两个都使用了mmseg来进行分词。据我了解,CoreSeek在支持细粒度的分词，而Sphinx-for-Chinese不支持。而公司使用的是Sphinx-for-Chinese,所以就遇到了分词的粒度问题。

根据产品人员的反馈，有许多这样的例子。例如搜索西海或者海岸时，搜不到大华西海岸酒店，搜索兵马俑时，搜不到秦始皇兵马俑博物馆,搜索肯尼亚时搜不到肯尼亚山。这都是因为Sphinx-for-Chinese使用mmseg得到最优结果后，就不在进行细分的结果。拿大华西海岸酒店这个例子来说，词典里有大华，西海岸，酒店，华西，西海，海岸这些词，根据mmseg得到的最优分词结果，分成大华+西海岸+酒店，这个分词的结果也是正确的，可是搜索西海，海岸就搜不到它的。问过Sphinx-for-Chinese的开发人员后，要想支持更细粒度的分词，只有修改源码。

在组长划出一条线，需要在哪一部分代码后，一个最简单的想法是，对于mmseg中每一步得到的最优结果，都进行更细粒度的划分。例如上面的例子，对于西海岸进行更细粒度划分后，就可以得到西海和海岸，这样搜索西海和海岸时，就可以搜索到。于是立马动手写，折腾一个上午后，果然可以搜到了，这样就达到了同城旅游中酒店搜索的效果了。可是搜索华西还是搜不到，而携程则可以搜到，在携程里，搜索西也可以搜到它。仔细考虑后，在原来的代码里只需要很少的修改就可以做到搜索华西是也可以搜到它，搜索效果已经超过了同程旅游。在增加单字索引后，搜索效果和携程相当接近。

相信许多使用Sphinx-for-Chinese都会遇到类似的问题，也都将用各自的办法解决这个问题。这里将这一部分代码开源，也算是对开源事业的一点点贡献。事实上，需要修改的地方并不是很多。这里我使用的是sphinx-for-chinese-2.2.1-dev-r4311版本,相信其它版本也可以进行类似的修改。需要修改的文件只有一个，那就是sphinx.cpp。

在2244行附近，class CSphTokenizer_UTF8Chinese : public CSphTokenizer_UTF8_Base这个类中,增加以下数据成员
``` c
int m_totalParsedWordsNum; //总共得到的分词结果
int m_processedParsedWordsNum; //已经处理的分词个数
int m_isIndexer; //标示是否是indexer程序
bool m_needMoreParser; //标示是否需要更细粒度分词
const char * m_pTempCur; //标示在m_BestWord中的位置
char m_BestWord[3 * SPH_MAX_WORD_LEN + 3]; //记录使用mmseg得到的最优分词结果
int m_iBestWordLength; //最优分词结果的长度
```

在6404行附近CSphTokenizer_UTF8Chinese<IS_QUERY>::CSphTokenizer_UTF8Chinese ()这个构造函数中，增加以下语句进行初始化。
``` c
 char *penv = getenv("IS_INDEXER");
        if (penv != NULL) {
                m_isIndexer = 1;
        } else {
                m_isIndexer = 0;
        }
        m_needMoreParser = false;
```
在6706行附近BYTE * CSphTokenizer_UTF8Chinese<IS_QUERY>::GetToken ()函数中int iNum;语句后面增加如下语句
``` c
       if(m_isIndexer && m_needMoreParser) { //对最优结果进行进一步细分
                while (m_pTempCur < m_BestWord + m_iBestWordLength) {
                        if(m_processedParsedWordsNum == m_totalParsedWordsNum) {
                                size_t minWordLength = m_pResultPair[0].length;
                                for(int i = 1; i < m_totalParsedWordsNum; i++) {
                                        if(m_pResultPair[i].length < minWordLength) {
                                                minWordLength = m_pResultPair[i].length;
                                        }
                                }
                                m_pTempCur += minWordLength;
                                m_pText=(Darts::DoubleArray::key_type *)(m_pCur + (m_pTempCur - m_BestWord));
                                iNum = m_tDa.commonPrefixSearch(m_pText, m_pResultPair, 256, m_pBufferMax-(m_pCur+(m_pTempCur-m_Best
Word)));
                                m_totalParsedWordsNum = iNum;
                                m_processedParsedWordsNum = 0;
                        } else {
                                iWordLength = m_pResultPair[m_processedParsedWordsNum].length;
                                m_processedParsedWordsNum++;
                                if (m_pTempCur == m_BestWord && iWordLength == m_iBestWordLength) { //是最优分词结果,跳过
                                        continue;
                                }
                                memcpy(m_sAccum, m_pText, iWordLength);
                                m_sAccum[iWordLength]='\0';

                                m_pTokenStart = m_pCur + (m_pTempCur - m_BestWord);
                                m_pTokenEnd = m_pCur + (m_pTempCur - m_BestWord) + iWordLength;
                                return m_sAccum;
                        }
                }
                m_pCur += m_iBestWordLength;
                m_needMoreParser = false;
                iWordLength = 0;
        }
```
在 iNum = m_tDa.commonPrefixSearch(m_pText, m_pResultPair, 256, m_pBufferMax-m_pCur);语句后面，增加如下语句 
``` c
            if(m_isIndexer && iNum > 1) {
                        m_iBestWordLength=getBestWordLength(m_pText, m_pBufferMax-m_pCur); //使用mmseg得到最优分词结果
                        memcpy(m_sAccum, m_pText, m_iBestWordLength);
                        m_sAccum[m_iBestWordLength]='\0';
                        m_pTokenStart = m_pCur;
                        m_pTokenEnd = m_pCur + m_iBestWordLength;

                        m_totalParsedWordsNum = iNum;
                        m_needMoreParser = true;
                        m_processedParsedWordsNum = 0;
                        memcpy(m_BestWord, m_pText, m_iBestWordLength);
                        m_BestWord[m_iBestWordLength]='\0';
                        m_pTempCur = m_BestWord;
                        return m_sAccum;
                }
```
需要修改的地方就这么多。重新编译，生成后indexer后,设置环境变量,export IS_INDEXER=1，重建索引即可。这里需要注意的一点是，必须使用修改代码之前的searchd，这样才会符合我们的需求，如果使用修改代码之后的searchd,搜索西海时，会分成西海，西，海，然后去搜索，这就不是我们想要的。

对于代码，有几个关键的地方需要分明的。
1.GetToken函数
这个行数每次返回一个词，也就是分词的结果，返回前，需要设置m_pTokenStart和m_pTokenEnd,标示这个词在内容中的开始位置和结束位置。当返回值为NULL时，标示分词结束

2.m_pCur
这个用来标示当前的指针在内容的偏移位置，前面说到的设置m_pTokenStart和m_pTokenEnd就需要用到这个值

3.commonPrefixSearch函数
调用这个函数会返回所有共同前缀的词，结果保存在m_pResultPair中。例如m_pText当前位置是西，则会返回西，西海，西海岸这三个有共同前缀的词。

4.getBestWordLength函数
这个函数使用mmseg算法，得到下次分词最优结果的长度。例如m_pText当前位置是西，最优分词结果是西海岸，而在utf-8中，一个字为三个字节，所以函数返回8。

因为代码简单，所以就不细说了。这个修改，唯一不足的是，无法做到精确匹配。也是说，假设两个地点，一个是北京，一个是北京大学，搜索北京时，无法保证北京是排在第一个，即使它和搜索词精确匹配。这是因为在对北京进行更细粒度分词时，将北京分成北京,北,京这个三个词，这样破坏了Sphinx用来判断精确匹配的一些设置。为了纠正这个错误，组长和我又写了一些代码，这部分新增的代码就没有上面那部分好理解了，同时写的也有一些别扭。
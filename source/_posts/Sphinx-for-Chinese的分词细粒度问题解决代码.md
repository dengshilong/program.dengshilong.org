title: Sphinx-for-Chinese的分词细粒度问题解决代码
tags:
  - Sphinx-for-chinese
  - 分词
  - 细粒度
id: 910
categories:
  - 搜索引擎
date: 2014-10-19 17:12:44
---

感觉上，这段代码不贴上来，仿佛欠别人钱似的。趁现在还有些精力，以后很长一段时间都不会接触Sphinx了，赶紧把这件事给做了。
具体为什么这样改，可以看前面的文章。以下修改是基于sphinx-for-chinese-2.2.1-dev-r4311版本，之需要修改sphinx.cpp即可。

在2296行后面添加如下代码：
``` 
struct CSphWord
{
    BYTE m_sAccum[3 * SPH_MAX_WORD_LEN + 3];
    int length;
    const BYTE *m_pTokenStart;
    const BYTE *m_pTokenEnd;
};
class ISphWords
{
public:
    int Length () const
    {
    return m_dData.GetLength();
    }

    const CSphWord * First () const
    {
    return m_dData.Begin();
    }

    const CSphWord * Last () const
    {
    return &m_dData.Last();
    }
    void Clean() {
    m_dData.Reset();
    }     

    void AddWord ( BYTE * word, int length, const BYTE *start, const BYTE *end)
    {
        CSphWord & tWord = m_dData.Add();
        memcpy(tWord.m_sAccum, word, length);
        tWord.length = length;
        tWord.m_pTokenStart = start;
        tWord.m_pTokenEnd = end;
    }

public:
    CSphVector<CSphWord> m_dData;
};
```

在2296行,`virtual int GetMaxCodepointLength () const { return m_tLC.GetMaxCodepointLength(); }`后面添加如下方法成员：
```
 cvirtual BYTE *          ProcessParsedWord();
```
在2303行，`Darts::DoubleArray::result_pair_type    m_pResultPair[256];`后面添加如下数据成员：
``` 
/*****add by luodongshan for indexer*****/
int totalParsedWordsNum; //总共需要处理的词
int processedParsedWordsNum; //已经处理的词
int isIndexer; //是否开启细粒度分词
bool needMoreParser; //需要更细粒度分词
const char * m_pTempCur;
char  m_BestWord[3 * SPH_MAX_WORD_LEN + 3];
int m_iBestWordLength;
ISphWords m_Words;
CSphWord *current;
bool isParserEnd;
```
在6448行，m_bHasBlend = false;后面添加如下初始化代码：
``` 
char *penv = getenv("IS_INDEX");
if (penv != NULL) {
    isIndexer = 1;
} else {
    isIndexer = 0;
}     
needMoreParser = false;
current = NULL;
isParserEnd = false;
```
在6743后面添加新增方法成员ProcessParsedWord的实现：
``` c
template < bool IS_QUERY >
BYTE * CSphTokenizer_UTF8Chinese<IS_QUERY>::ProcessParsedWord() {
    for (; current != NULL && current <= m_Words.Last(); ) {
    memcpy(m_sAccum, current->m_sAccum, current->length);
    m_pTokenStart = current->m_pTokenStart;
    m_pTokenEnd = current->m_pTokenEnd;
    current++;
    return m_sAccum;
    }
    isParserEnd = false;
    m_Words.Clean();
    current = NULL;
    return NULL;
}
```
在6785行， `bool bGotSoft = false; // hey Beavis he said soft huh huhhuh `后面增加如下代码：
``` c
    if (isIndexer && isParserEnd) { //使用MMSEG分词结束，处理细粒度分词得到的词
        return ProcessParsedWord();
    }  
```
在6791行， int iNum;后面增加如下代码：
``` c
    /***add by dengsl 2014/06/24****/
    if(isIndexer && needMoreParser) { //对最优匹配进行细粒度分词
        while (m_pTempCur < m_BestWord + m_iBestWordLength) {
            if(processedParsedWordsNum == totalParsedWordsNum) { //此位置的前缀词已处理完，跳到下一位置
                size_t minWordLength = m_pResultPair[0].length;
                for(int i = 1; i < totalParsedWordsNum; i++) {
                    if(m_pResultPair[i].length < minWordLength) {
                        minWordLength = m_pResultPair[i].length;
                    }     
                }     
                m_pTempCur += minWordLength;
                m_pText=(Darts::DoubleArray::key_type *)(m_pCur + (m_pTempCur - m_BestWord));
                iNum = m_tDa.commonPrefixSearch(m_pText, m_pResultPair, 256, m_pBufferMax-(m_pCur+(m_pTempCur-m_BestWord)));
                totalParsedWordsNum = iNum;
                processedParsedWordsNum = 0;
            } else {
                iWordLength = m_pResultPair[processedParsedWordsNum].length;
                processedParsedWordsNum++;
                if (m_pTempCur == m_BestWord && iWordLength == m_iBestWordLength) {
                    continue;
                }     
                memcpy(m_sAccum, m_pText, iWordLength);
                m_sAccum[iWordLength] = '\0';
                if( 3 * SPH_MAX_WORD_LEN + 3 >= iWordLength + 2) {
                    m_sAccum[iWordLength + 1] = '\0';
                    if(m_pTokenEnd == m_pBufferMax) { //是结尾，保存结尾符标志
                        m_sAccum[iWordLength + 1] = 1;
                    }     
                }     
                m_Words.AddWord(m_sAccum, iWordLength + 2, m_pCur + (m_pTempCur - m_BestWord), m_pCur + (m_pTempCur - m_BestWord) + iWordLength);
            }     
        }     
        m_pCur += m_iBestWordLength;
        needMoreParser = false;
        iWordLength = 0;
        current = const_cast< CSphWord * > ( m_Words.First() );
    }     
    /***add end by dengsl 2014/06/24****/
```
在6832行，iNum = m_tDa.commonPrefixSearch(m_pText, m_pResultPair, 256, m_pBufferMax-m_pCur);后面增加如下代码：
``` 
        /***add by dengsl 2014/06/24****/
        if(isIndexer && iNum > 1) {
            m_iBestWordLength=getBestWordLength(m_pText, m_pBufferMax-m_pCur);
            memcpy(m_sAccum, m_pText, m_iBestWordLength);
            m_sAccum[m_iBestWordLength]='\0';
            m_pTokenStart = m_pCur;
            m_pTokenEnd = m_pCur + m_iBestWordLength;

            totalParsedWordsNum = iNum;
            needMoreParser = true;
            processedParsedWordsNum = 0;
            memcpy(m_BestWord, m_pText, m_iBestWordLength);
            m_BestWord[m_iBestWordLength]='\0';
            m_pTempCur = m_BestWord;
            if( 3 * SPH_MAX_WORD_LEN + 3 >= m_iBestWordLength + 2) {
                m_sAccum[m_iBestWordLength + 1] = '\0';
                if(m_pTokenEnd == m_pBufferMax) { //是结尾，保存结尾符标志
                    m_sAccum[m_iBestWordLength + 1] = 1;
                }     
            }     
            return m_sAccum;
        }     
        /***add by dengsl 2014/06/24****/
```
在6903行，将
``` 
return NULL;
```
修改为
``` 
/* dengsl */
isParserEnd = true;
return ProcessParsedWord();
```
在6914行，将
``` 
if_const ( IS_BLEND && !BlendAdjust ( pCur ) )
   return NULL;
```
修改成：
``` 
/* dengsl */
if_const ( IS_BLEND && !BlendAdjust ( pCur ) ) {
    isParserEnd = true;
    return ProcessParsedWord();
}  
```
在27210行，m_tHits.AddHit ( uDocid, iWord, m_tState.m_iHitPos );后面增加如下代码：
``` 
///add by luodongshan 20140626
if(sWord != NULL) {
    int sWord_len = strlen((char*)sWord);
    if(sWord_len + 2 <= 3 * SPH_MAX_WORD_LEN + 3 && sWord[sWord_len + 1] == 1 &&
        getenv("IS_INDEX") != NULL && !bSkipEndMarker )  {
    CSphWordHit * pHit = const_cast < CSphWordHit * > ( m_tHits.Last() );
    HITMAN::SetEndMarker ( &pHit->m_iWordPos );

    }     
}     
///add by luodongshan 20140626 end
```
将过上面的修改，重新编译源码，之后设置环境变量IS_INDEX,即运行export IS_INDEX=1,就可以支持细粒度的划分。

一个需要注意的地方是,对于searchd,也变成细粒度分词了，这并不是我们想要的，所以对于searchd，需要使用未修改代码的searchd.因为我们想建索引时细粒度，搜索时粗粒度。

之所以要这样，是因为如果不这样处理，很多结果会搜出来了。如有文章内容分别为中大酒店，中大假日酒店。如果搜索时也是细粒度，则有中大，酒店，中，大，大酒店，酒，店等查询词，而大酒店只在中大酒店中存在，所以只会搜出中大酒店，这并不是我们想要的。

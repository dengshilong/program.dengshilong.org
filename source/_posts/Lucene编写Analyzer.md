title: Lucene编写Analyzer
date: 2015-12-23 12:01:07
tags: Lucene
categories: Lucene
---
在有些应用中，需要针对应用的特征编写Analyzer，这里以Lucene5.0为例。在许多中文搜索应用，往往需要对文本进行分词，而用单字分词不能满足条件，所以需要使用其它分词，而MMSEG是其中一种。

从网上找到了chenbl写的[mmseg4j](https://github.com/chenlb/mmseg4j-core)，学会如何使用mmseg4j后，开始编写Analyzer。查看[Analysis包](https://lucene.apache.org/core/5_4_0/core/org/apache/lucene/analysis/package-summary.html#package_description)的介绍后，发现主要是实现一个Tokenizer，然后在Analyzer中调用即可。于是编写了如下MMSegAnalyzer,
```
public class MMSegAnalyzer extends Analyzer {
    public MMSegAnalyzer() {
    }
    @Override
    protected TokenStreamComponents createComponents(String fieldName) {
        // TODO Auto-generated method stub
        return new TokenStreamComponents(new MMSegTokenizer());
    }
}
```
之后编写MMSegTokenizer,
```
public class MMSegTokenizer extends Tokenizer {
    private final CharTermAttribute termAtt = addAttribute(CharTermAttribute.class);
    private final OffsetAttribute offsetAtt = addAttribute(OffsetAttribute.class);
    Dictionary dic;
    Seg seg;
    MMSeg mmSeg;

    public MMSegTokenizer() {
        dic = Dictionary.getInstance();
        seg = new ComplexSeg(dic);
        mmSeg = new MMSeg(input, seg);
    }

    @Override
    public boolean incrementToken() throws IOException {
        clearAttributes();
        // TODO Auto-generated method stub
        Word word = null;
        while((word = mmSeg.next())!=null) {
            termAtt.copyBuffer(word.getSen(), word.getWordOffset(), word.getLength());
            offsetAtt.setOffset(word.getStartOffset(), word.getEndOffset());
            return true;
        }
        return false;
    }
    @Override
    public void close() throws IOException {
        super.close();
    }

    @Override
    public void reset() throws IOException {
        super.reset();
    }
}
```
其中
```
private final CharTermAttribute termAtt = addAttribute(CharTermAttribute.class);
private final OffsetAttribute offsetAtt = addAttribute(OffsetAttribute.class);
```
这两个属性是用来设置Token的内容和文本的偏移位置。
然后使用《Lucene in Action2》第四章中提到的AnalyzerDemo.java来进行测试，发现抛出异常java.lang.IllegalStateException: TokenStream contract violation，
查看TokenStream类后,知道reset函数是在incrementToken函数之前调用，主要是完成一些初始化工作。猜测是MMSeg有一些初始化工作没有完成，然后查看MMSeg类，发现有个reset函数，正是完成一些初始化工作。
于是修改修改MMSegTokenizer的reset函数，如下:
```
public class MMSegTokenizer extends Tokenizer {
    private final CharTermAttribute termAtt = addAttribute(CharTermAttribute.class);
    private final OffsetAttribute offsetAtt = addAttribute(OffsetAttribute.class);
    Dictionary dic;
    Seg seg;
    MMSeg mmSeg;

    public MMSegTokenizer() {
        dic = Dictionary.getInstance();
        seg = new ComplexSeg(dic);
        mmSeg = new MMSeg(input, seg);
    }

    @Override
    public boolean incrementToken() throws IOException {
        clearAttributes();
        // TODO Auto-generated method stub
        Word word = null;
        while((word = mmSeg.next())!=null) {
            termAtt.copyBuffer(word.getSen(), word.getWordOffset(), word.getLength());
            offsetAtt.setOffset(word.getStartOffset(), word.getEndOffset());
            return true;
        }
        return false;
    }
    @Override
    public void close() throws IOException {
        super.close();
    }

    @Override
    public void reset() throws IOException {
        super.reset();
        mmSeg.reset(input);
    }
}
```
MMSegAnalyzer可以进行分词了。之后看mmseg4j的实现，才发现要实现一个高效的MMSEG分词并不是一件容易的事。

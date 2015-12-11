title: Sphinx-for-Chinese的分词细粒度问题(续)
tags:
  - Sphinx-for-chinese
  - SPH_RANK_SPH04
  - 分词粒度
  - 精确匹配
id: 781
categories:
  - 搜索引擎
date: 2014-07-08 21:11:45
---

在[Sphinx-for-Chinese的分词细粒度问题](http://program.dengshilong.org/2014/06/28/sphinx-for-chinese的分词细粒度问题/)中说过，为了解决分词的粒度问题，我们对Sphinx-for-Chinese的代码进行了一些修改，而针对精确匹配我们也写了一些额外的代码，虽然这一部分的代码并不是很好看，但毕竟解决了问题，所以也想对这一部分进行说明，因为相信其他人也会遇到类似的问题，这里可以提供一个参考的解决方案。

所谓精确匹配，也就是搜索的词语搜索的字段完全相同。例如假设有三个标题,中大，中大酒店，中大假日酒店，则搜索中大时，与中大完全匹配。一般情况下，我们都希望精确匹配的内容排在前面，此时还需要设置排序方法为SPH_RANK_SPH04。

依然以sphinx-for-chinese-2.2.1-dev-r4311为例，在sphinxsearch.cpp中6282行附近，找到RankerState_ProximityBM25Exact_fn，这里就是sph04的实现。看到数据成员m_uExactHit，知道这个与精确匹配有关，在这段代码里看到HITMAN::IsEnd，于是猜测在某个地方有SetEnd,在sphinx.cpp中27144行附近找到CSphSource_Document::BuildRegularHits方法，在这里找到了，
CSphWordHit * pHit = const_cast < CSphWordHit * > ( m_tHits.Last() );
HITMAN::SetEndMarker ( &pHit->m_iWordPos );
于是我们想，在进行细粒度分词时，中大将被分成，中大、中、大三个词。只要有某种办法，将中大这个词也使用SetEndMarker就可以达到所要的目的，于是增加了一些代码。

这之后，搜索中大时，中大这个标题确实排在了前面，可是问题又出现了，在搜索中大酒店时，中大酒店这个标题并没有排在前面，中大酒店与中大假日酒店的权重是相同的。分析了原因，搜索中大酒店时，将被分成中大+酒店，而中大假日酒店中，正好也包含中大和酒店，并且酒店也是排在末尾，于是这两个的权重是一样的。于是我们只好再看看m_uExactHit的计算，发现IsEnd并不是唯一的条件，于是相信为细分以前，索引中大酒店时，分词的词是中大、酒店，而细分后变成了中大、中、大、大酒店、酒店、酒、店，于是我们猜测，如果将分词按照原先的方法分一次，之后再一起返回细粒度的分词，可能可以达到目的。这样的结果就是分词返回的是中大、酒店、中、大、大酒店、酒、店。于是按照这个想法，又增加了一些代码。果然这次搜索中大酒店时，中大酒店排在了前面，并且权重比中大假日酒店高。
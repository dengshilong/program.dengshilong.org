title: Elasticsearch中ik添加同义词
date: 2016-04-06 20:13:49
tags: 
    - Elasticsearch
    - ik
categories:
    - 搜索引擎
---
参考[http://elasticsearch.cn/?/question/29](http://elasticsearch.cn/?/question/29)

## 配置synonym.txt
在config目录下analysis,在analysis目录里新建synonym.txt文件,内容如下
```
beijing,北京,帝都
上海,魔都
```
## 配置elasticsearch.yml
在elasticsearch.yml里添加
```
index:
    analysis:
        filter:
            my_synonym:
                type: synonym
                synonyms_path: analysis/synonym.txt
        analyzer:
            ik_smart_syno:
                type: custom
                tokenizer: ik_smart
                filter: [my_synonym]
            ik_max_word_syno:
                type: custom
                tokenizer: ik_max_word
                filter: [my_synonym]
```

## 测试
新建索引`curl -XPUT 'localhost:9200/test?pretty'`,之后执行`http://localhost:9200/test/_analyze?analyzer=ik_max_word_syno&text=上海外滩`


title: Elasticsearch修改版本号和日志
date: 2016-04-16 20:51:18
tags: 
    - Elasticsearch
categories:
    - 搜索引擎
---
## 修改版本号
在[https://github.com/elastic/elasticsearch/releases](https://github.com/elastic/elasticsearch/releases)里下载到v2.3.0的Elasticsearch, 编译后得到的是2.3.0-SNAPSHOT, 这在pom.xml文件里有体现，于是进行替换
```
find . -name "pom.xml" | xargs sed -i '' 's/2.3.0-SNAPSHOT/2.3.0/g'
```
这里sed的用法是在Mac电脑上。

但Elasticsearch无法启动，报错说还是2.3.0-SNAPSHOT, 打开Version.java, 将
```
public static final Version V_2_3_0 = new Version(V_2_3_0_ID, true, org.apache.lucene.util.Version.LUCENE_5_5_0);
```
修改为
```
public static final Version V_2_3_0 = new Version(V_2_3_0_ID, false, org.apache.lucene.util.Version.LUCENE_5_5_0);
```
编译后可以正常启动.

## 修改日志格式
目前Elasticsearch的日志输出无法知道是哪个类，哪个包，第几行打印的日志，所以需要修改logging.yml的配置。

将
```
conversionPattern: "[%d{ISO8601}][%-5p][%-25c]: %m%n"
```
改为
```
conversionPattern: "[%d{ISO8601}][%-5p][%l]: %m%n"
```

## 输出query日志
想知道用户的query日志，但Elasticsearch没有记录，在NettyHttpRequest.java里, `String uri = request.getUri();`后添加
```
try {
    logger.info("### query uri {}", URLDecoder.decode(uri, "UTF-8"));
} catch (java.io.UnsupportedEncodingException e) {
    logger.info("### query uri {}", uri);
}
```

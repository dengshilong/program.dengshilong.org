title: Wordpress迁移到Hexo遇到的问题
date: 2015-12-11 15:53:24
tags:
---
因为在这个学习笔记里要贴一些代码，可是Wordpress的编辑器对于代码支持不够好，会改变代码格式，于是决定迁移到对代码支持更好的Hexo.Hexo是用Node.js写的博客系统，类似与Octpress，台湾人写的，很不错。

对于如何搭建Hexo，以及如何迁移Wordpress,可以看官方文档。这里主要说说迁移过程遇到的问题。

## Template render error: unexpected token: / 
在[https://github.com/hexojs/hexo/issues/1439](https://github.com/hexojs/hexo/issues/1439)也有类似的问题，原来hexo变量是用两个{和两个}包含起来, 而在一些编程语言中，二维数组会出现用两个{和两个}的情况，所以冲突了。于是修改hexo-migrator-wordpress插件,到存放hexo-migrator-wordpress插件的目录(从博客的根目录进入到node_modules/hexo-migrator-wordpress)下,打开index.js, 增加一个函数
```
function replaceTwoBrace(str){
    str = str.replace(/{{/g, '{ {');
    return str;
};
```
之后在`content = tomd(content).replace(/\r\n/g, '\n');`前面增加一行`content = replaceTwoBrace(content);`,解决问题。

## 文件名问题
生成的文件名如下例子 
e8-af-ad-e8-a8-80-e7-89-b9-e6-80-a7-e8-bf-98-e6-98-af-e6-9c-89-e5-bf-85-e8-a6-81-e5-ad-a6-e4-b9-a0-e7-9a-84.md
e8-bd-af-e8-bf-9e-e6-8e-a5-e5-92-8c-e7-a1-ac-e8-bf-9e-e6-8e-a5.md
e8-bf-bd-e8-b8-aaquery-too-complex-not-enough-stack-e9-94-99-e8-af-af.md
我想这是将URL转化过来的结果，因为URL中，中文是UTF-8编码。这里之所以有问题是因为这样的文件名生成的URL和以前在Wordpress中不一样，因为多一个'-'符号.想通过修改hexo-migrator-wordpress插件来解决,打开index.js, 在128行附近的`post.create(data, next);`, 之后看到`post = hexo.post;`, 然后进入node_modules/hexo/lib/hexo目录，在post.js里看到`fs.writeFile(path, content)`，想通过改这里来解决。后来想想，写个Python脚本,从内容的第一行，也就是title字段抽取出标题也可以解决。于是写了个Python脚本, changePostURL.py
```
import os,sys

def getTitle(firstLine):
    strs = ':'.join(firstLine.split(':')[1:])
    strs = strs.replace("'", '') 
    strs = strs.strip()
    title = '-'.join(strs.split(' '))
    return title
if __name__ == "__main__":
    dirName = sys.argv[1]
    for root,dirs,fileNames in os.walk(dirName):
        for fileName in fileNames:
            print fileName 
            print root
            fileName = os.path.join(root, fileName)
            f = open(fileName)
            firstLine = f.readline()
            title = getTitle(firstLine)
            print title
            content = firstLine + f.read()
            f.close()
            newname = title + '.md'
            print newname
            os.rename(fileName, os.path.join(root,newname))
```
执行`python changePostURL.py source/_posts/`搞定

## HTML实体问题
在转化出来的文件内容中，有&gt;和&lt;等实体，我想是因为Wordpress编辑器进行了转化。虽然最后的显示结果没有问题，但在Markdown中，我还是希望看到>和<等,于是在hexo-migrator-wordpress中再添加一个函数.
```
function replaceHTMLEntity(str){
    str = str.replace(/amp;/g, '');
    str = str.replace(/&lt;/g, '<');
    str = str.replace(/&gt;/g, '>');
    str = str.replace(/&quot;/g, '"');
    str = str.replace(/&#92;/g, '\\');
    str = str.replace(/&#48;/g, '0');
    return str;
};
```
之后在`content = tomd(content).replace(/\r\n/g, '\n');`前面添加一行,`content = replaceHTMLEntity(content);`，解决问题

## 代码标签问题
在Wordpress中，我使用Syntax Highlighter进行代码高亮时，在代码块的前后需要添加相应的标签来高亮，如Java程序需要添加[java],[/java], 而在Markdown中这些标签就不需要了，需要对它进行替换。添加一个函数
```
function replaceCodeTag(str){
    str = str.replace(/\[python\]/gi, '```');
    str = str.replace(/\[\/python\]/gi, '```');
    str = str.replace(/\[java\]/gi, '```');
    str = str.replace(/\[\/java\]/gi, '```');
    str = str.replace(/\[php\]/gi, '```');
    str = str.replace(/\[\/php\]/gi, '```');
    str = str.replace(/\[c\]/gi, '```');
    str = str.replace(/\[\/c\]/gi, '```');
    return str;
};
```
之后在`content = tomd(content).replace(/\r\n/g, '\n');`前面添加一行,`content = replaceCodeTag(content);`，解决问题

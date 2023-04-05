title: ChatGPT真是不错的学习工具
date: 2023-04-05 21:45:54
tags:
    - ChatGPT
    - jsdom
categories:
---
虽然知道ChatGPT厉害，但一直没有时间去注册个账号玩玩，最近终于有时间了，注册了个账号体验了下，真心不错。

之前群友提了个正则表达式的问题，用正则表达式匹配出现2次及2次以上的字符，这个问题读大学的时候舍友郭老曾经问过我，作为曾经的正则小王子，当时就知道要用反向引用，现在当然也知道。和群友说了下这可得用到正则的高级用法，可以看一下反向引用，一会儿他问了ChatGPT，就给他解答了。现在拿着这个问题问ChatGPT, 得到如下答案。

要匹配出现2次及2次以上的字符，可以使用正则表达式中的花括号 {} 来指定匹配次数。

假设要匹配的字符串为 hellooo worlddd，我们可以使用如下的正则表达式来匹配出现2次及2次以上的字符：
(.)\1{1,}
这个正则表达式的含义是：匹配任意一个字符 (.)，然后匹配和它相同的字符至少1次 {1,}。其中 \1 表示反向引用前面匹配的字符，也就是 \1 所在的位置应该与前面 (.) 所匹配的字符相同。

去年初在学习js补环境的时候，想知道在jsdom中如何在解析页面前执行js代码的办法，找了一圈没找到答案。买了猿人学的课，看了所有的js视频，最终找到了解决的办法，也就是beforeParse方法，如今把这个问题丢给ChatGPT, 就能得到答案。

在使用 jsdom 解析 HTML 页面之前，你可以通过设置 beforeParse 选项来在解析之前执行 JavaScript 代码。

具体来说，你可以创建一个 JSDOM 对象并设置 beforeParse 选项为一个回调函数，在这个回调函数中编写需要执行的 JavaScript 代码。例如：

```
const jsdom = require("jsdom");
const { JSDOM } = jsdom;

const html = "<html><body><div id='myDiv'></div></body></html>";
const options = {
  beforeParse(window) {
    // 在这里执行需要在解析页面前执行的 JavaScript 代码
    const myDiv = window.document.getElementById("myDiv");
    myDiv.textContent = "Hello, world!";
  }
};

const dom = new JSDOM(html, options);
console.log(dom.window.document.querySelector("#myDiv").textContent);
// Output: "Hello, world!"
```

在这个例子中，我们创建了一个包含一个空 div 元素的 HTML 页面，并设置了 beforeParse 选项为一个回调函数。在这个回调函数中，我们使用 getElementById 方法获取了这个 div 元素，并将其文本内容设置为了 "Hello, world!"。然后我们创建了一个 JSDOM 对象并传入了这个 HTML 页面和选项对象，最后我们验证了修改后的 div 元素的文本内容是否正确。

注意，beforeParse 回调函数只能在 JSDOM 对象创建时执行一次，无法在解析完成后再次执行。如果你需要在解析完成后执行 JavaScript 代码，可以使用 window.onload 或 window.addEventListener 等方法。

前几天前同事又问了个算法题，写一个函数split_text，参数一个是字符串text 一个是列表 dic,都是英文单词 返回一个列表 每个元素都是一个英文单词，并且顺序连起来，就是text 比如 split_text('appledesktop', ['a', 'app', 'apple', 'desk', 'top', 'led']) 返回 ['apple', 'desk', 'top'] split_text('appledappleatop', ['a', 'app', 'apple', 'desk', 'top', 'led']) 返回 ['app', 'led', 'apple', 'a', 'top']


您可以使用动态规划来解决这个问题。首先，创建一个长度为text长度+1的列表dp，dp[i]表示text[0:i]的分割结果。初始化dp[0]=[]。然后，从i=1开始，遍历dp列表。对于每个i，从j=i-1到j=0倒序遍历。如果text[j:i]在字典dic中，那么将dp[i]更新为dp[j]加上[text[j:i]]。最后返回dp[-1]作为结果即可。

下面是实现这个函数的代码：

```
def split_text(text, dic):
    dp = [[] for _ in range(len(text) + 1)]
    dp[0] = []

    for i in range(1, len(dp)):
        for j in range(i - 1, -1, -1):
            if text[j:i] in dic:
                if dp[j]:
                    dp[i] = dp[j] + [text[j:i]]
                    break
                else:
                    dp[i] = [text[j:i]]
    return dp[-1]
```

您可以运行一些测试来验证函数是否正常工作：

```
text = 'appledesktop'
dic = ['a', 'app', 'apple', 'desk', 'top', 'led']
print(split_text(text, dic))  # ['apple', 'desk', 'top']

text = 'appledappleatop'
dic = ['a', 'app', 'apple', 'desk', 'top', 'led']
print(split_text(text, dic))  # ['app', 'led', 'apple', 'a', 'top']
```

问ChatGPT，还有更优的办法吗？它又给出了回答。

上面给出的动态规划方法是一个不错的解决方案，但是也可以使用更简单和更高效的贪心算法来解决这个问题。

具体来说，对于给定的文本字符串text和字典列表dic，我们可以考虑从text的左侧开始遍历，每次查找能够匹配字典中某个单词的最长前缀，并将该单词加入结果列表中。重复这个过程，直到text被完全分割成单词为止。

下面是实现这个贪心算法的代码：

```
def split_text(text, dic):
    result = []
    i = 0

    while i < len(text):
        found = False
        for word in dic:
            if text.startswith(word, i):
                result.append(word)
                i += len(word)
                found = True
                break
        if not found:
            # 如果在字典中找不到匹配的单词，则返回空列表。
            return []
    return result
```

真的是强到离谱，这之后用搜索引擎的频率就低很多了。

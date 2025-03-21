title: 听闻sdenv被反爬
date: 2025-03-17 18:51:31
tags:
    - jsdom
    - sdenv
    - 逆向
    - 爬虫
    - 反爬
    - JavaScript
categories:
---
听闻sdenv被反爬，垂死病中惊坐起，去看了下sdenv的源码, 整理了下以前写的针对jsdom检测的简单测试代码

```
const jsdom = require("jsdom");  // 引入 jsdom
const { JSDOM } = jsdom;  // 引出 JSDOM 类， 等同于 JSDOM = jsdom.JSDOM
const userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
const resourceLoader = new jsdom.ResourceLoader({
  userAgent: userAgent
});
let dom = new JSDOM(``, {
    url: "https://example.org/",
    referrer: "https://example.com/",
   resources: resourceLoader,
});
window = dom.window;
debugger;
console.log(window.navigator.userAgent);

function detectForm(document) {
    let url = 'https://www.baidu.com/'
    let form = document.createElement('form');
    form.action = '';
    let input = document.createElement('input');
    input.name = 'action';
    form.appendChild(input)
    input = document.createElement('input');
    input.name = 'textContent';
    input.id = 'password';
    form.appendChild(input)
    return form.action != url && form.action.__proto__.toString() == '[object HTMLInputElement]'
}

console.log('test _globalObject', (typeof window._globalObject != "undefined" && typeof window != "undefined" && window._globalObject == window) === false);
console.log('test document ', window.document.toString() === '[object HTMLDocument]')
console.log('test open ', window.open.toString() === 'function open() { [native code] }')
console.log('test fetch ', window.fetch !== undefined && window.fetch.toString() === 'function fetch() { [native code] }')
console.log('test prompt ', window.prompt.toString() === 'function prompt() { [native code] }')
console.log('test Event ', window.Event.toString() === 'function Event() { [native code] }')
console.log('test Request', window.Request !== undefined && window.Request.toString() === 'function Request() { [native code] }')
console.log('test XPathException',  window.XPathException === undefined)
console.log('test webdriver ', window.navigator.webdriver === false)
console.log('test webdriver ', (Object.getOwnPropertyDescriptor(window.navigator.__proto__, 'webdriver') && Object.getOwnPropertyDescriptor(window.navigator.__proto__, 'webdriver').get.toString()) === 'function get webdriver() { [native code] }')
console.log('test document.all ', typeof window.document.all === 'undefined')
console.log('test document.all ', window.document.all !== undefined && (window.document.all.__proto__.toString() === '[object HTMLAllCollection]'))
console.log('test form ', detectForm(window.document) === true)
```

针对sdenv, 写了一个简单的测试代码，放在sdenv源码的example目录下跑

```
const {
    jsdomFromText
} = require('../utils/jsdom');
const browser = require('../browser/');

let index_url = "https://www.example.com/"
const [jsdomer, cookieJar] = jsdomFromText({
            url: `${index_url}`,
            referrer: `${index_url}`,
            contentType: "text/html",
            runScripts: 'dangerously',
            beforeParse(window) {
                browser(window, 'chrome')
            },
        })

const dom = jsdomer('<html></html>');
window = dom.window;

debugger;
console.log(window.navigator.userAgent);
function detectForm(document) {
    let url = 'https://www.baidu.com/'
    let form = document.createElement('form');
    form.action = '';
    let input = document.createElement('input');
    input.name = 'action';
    form.appendChild(input)
    input = document.createElement('input');
    input.name = 'textContent';
    input.id = 'password';
    form.appendChild(input)
    return form.action != url && form.action.__proto__.toString() == '[object HTMLInputElement]'
}

console.log('test _globalObject', (typeof window._globalObject != "undefined" && typeof window != "undefined" && window._globalObject == window) === false);
console.log('test document ', window.document.toString() === '[object HTMLDocument]')
console.log('test open ', window.open.toString() === 'function open() { [native code] }')
console.log('test fetch ', window.fetch !== undefined && window.fetch.toString() === 'function fetch() { [native code] }')
console.log('test prompt ', window.prompt.toString() === 'function prompt() { [native code] }')
console.log('test Event ', window.Event.toString() === 'function Event() { [native code] }')
console.log('test Request', window.Request !== undefined && window.Request.toString() === 'function Request() { [native code] }')
console.log('test XPathException',  window.XPathException === undefined)
console.log('test webdriver ', window.navigator.webdriver === false)
console.log('test webdriver ', (Object.getOwnPropertyDescriptor(window.navigator.__proto__, 'webdriver') && Object.getOwnPropertyDescriptor(window.navigator.__proto__, 'webdriver').get.toString()) === 'function get webdriver() { [native code] }')
console.log('test document.all ', typeof window.document.all === 'undefined')
console.log('test document.all ', window.document.all !== undefined && (window.document.all.__proto__.toString() === '[object HTMLAllCollection]'))
console.log('test form ', detectForm(window.document) === true)
```

测试结果如下

```
test _globalObject true
test document  false
test open  false
test fetch  true
test prompt  false
test Event  true
test Request true
test XPathException true
test webdriver  true
test webdriver  true
test document.all  true
test document.all  false
test form  true
```

可以看到几个测试结果是false的，而浏览器里都是true, 得针对修改下

title: 用Playwright和Express写了个浏览器渲染服务
date: 2025-09-21 19:25:12
tags:
    - 爬虫
    - 自动化
categories:
---
声明: 本文章中所有内容仅供学习交流使用，不用于其他任何目的，不提供完整代码。抓包内容、敏感网址、数据接口等均已做脱敏处理，严禁用于商业用途和非法用途，否则由此产生的一切后果均与作者无关！若有侵权，请在公众号 【静夜随想】 联系作者立即删除！

[用Playwright和Flask写了个浏览器渲染服务](https://mp.weixin.qq.com/s/mdEWOCv6-JC1PO1i2hSDVw)后，测试下来会有内存泄漏的现象，同时也发现它最终是调用 Node 的 Playwright库来实现浏览器渲染。那么我还不如直接用Node 的 Playwright 库来写一个渲染服务，这样应该速度会更快，也可能不会有内存泄漏。

于是又让AI吭哧吭哧的写了一段代码，代码如下

```
const express = require('express');
const bodyParser = require('body-parser');
const {
    chromium
} = require('playwright');
// 初始化 Express 应用
const app = express();
const PORT = process.env.PORT || 3000;
// 中间件
app.use(bodyParser.json({
    limit: '100mb'
}));
app.use(bodyParser.urlencoded({
    limit: '100mb',
    extended: true
}));
// 保持一个持久的浏览器实例以提高性能
let browser;
// 初始化 playwright 浏览器
async function initializeBrowser() {
    try {
        browser = await chromium.launch({
            headless: true,
            args: [
                '--no-sandbox',
            ]
        });
        console.log('playwright browser initialized successfully');
    } catch (error) {
        console.error('Failed to initialize playwright browser:', error);
        throw error;
    }
}
// 创建延迟函数 - 强制等待指定毫秒数
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
// 将cookies数组转换为字典（键值对）
function convertCookiesToDict(cookies) {
    const cookieDict = {};
    if (Array.isArray(cookies)) {
        cookies.forEach(cookie => {
            // 使用cookie的name作为键，value作为值
            if (cookie.name && cookie.value !== undefined) {
                cookieDict[cookie.name] = cookie.value;
            }
        });
    }
    return cookieDict;
}
app.post('/get-cookies', async (req, res) => {
    const {
        url,
        html,
        user_agent
    } = req.body;
    if (!url || !html) {
        return res.status(400).json({
            error: '请同时提供url和html参数'
        });
    }
    let page;
    try {
        // 配置页面选项，包括可选的userAgent
        const pageOptions = {};
        if (user_agent) {
            pageOptions.userAgent = user_agent;
            console.log(`使用自定义User-Agent: ${user_agent}`);
        }
        // 使用配置选项创建新页面
        page = await browser.newPage(pageOptions);
        // 设置路由拦截 - 拦截所有请求
        await page.route('**/*', async (route, request) => {
            // 获取当前请求的URL
            const requestUrl = request.url();
            // 检查当前请求是否匹配目标URL
            if (requestUrl == url) {
                // 对目标URL返回自定义HTML
                await route.fulfill({
                    status: 200,
                    content_type: 'text/html',
                    body: html
                });
                console.log(`已处理目标URL请求: ${requestUrl}`);
            } else {
                // 其他所有请求都直接终止
                await route.abort('aborted');
                console.log(`已终止非目标URL请求: ${requestUrl}`);
            }
        });
        // 导航到目标URL，此时会被我们的路由拦截处理
        await page.goto(url, {
            timeout: 30000
        });
        // 获取并返回Cookie
        let cookies = await page.context().cookies();
        cookies = convertCookiesToDict(cookies);
        res.json({
            success: true,
            cookies: cookies,
        });
    } catch (error) {
        console.error('处理请求时出错:', error);
        res.status(500).json({
            success: false,
            error: error.message
        });
    } finally {
        if (page) {
            await page.close();
        }
    }
});
// 启动服务器并初始化浏览器
async function startServer() {
    try {
        await initializeBrowser();
        app.listen(PORT, () => {
            console.log(`JavaScript execution service running on port ${PORT}`);
            console.log(`API endpoints:`);
            console.log(`- POST /get-cookies: Execute JavaScript code`);
        });
    } catch (error) {
        console.error('Failed to start server:', error);
        process.exit(1);
    }
}
// 处理进程退出，确保浏览器正确关闭
process.on('SIGINT', async () => {
    console.log('Shutting down...');
    if (browser) {
        await browser.close();
    }
    process.exit(0);
});
// 启动服务
startServer();
```

代码都放在Github仓库https://github.com/dengshilong/browser_server里了，有兴趣的可以看看。

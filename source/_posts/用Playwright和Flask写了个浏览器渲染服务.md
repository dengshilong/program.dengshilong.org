title: 用Playwright和Flask写了个浏览器渲染服务
date: 2025-09-21 19:23:48
tags:
    - 爬虫
    - 自动化
categories:
---
声明: 本文章中所有内容仅供学习交流使用，不用于其他任何目的，不提供完整代码。抓包内容、敏感网址、数据接口等均已做脱敏处理，严禁用于商业用途和非法用途，否则由此产生的一切后果均与作者无关！若有侵权，请在公众号 【静夜随想】 联系作者立即删除！
最近对浏览器自动化热情越来越高，于是想用浏览器来取代之前的补环境方案。借助越来越强的AI能力，写写提示词，让它写了一个渲染服务。

```
import json
import time
from playwright.sync_api import sync_playwright
from flask import Flask, jsonify, request
app = Flask(__name__)
playwright = sync_playwright().start()
browser = playwright.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
            ])
def generate_cookies(url, html, user_agent=None):
    default_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    if user_agent:
        default_user_agent = user_agent
    context = browser.new_context(
        user_agent=default_user_agent,
    )
    page = context.new_page()
    def handle_request(route, request):
        print('hererer ', request.url, url)
        if url in request.url:
            # 返回自定义的 HTML 内容
            route.fulfill(status=200, content_type='text/html', body=html)
        else:
            route.abort()
    page.route("**/*", handler=handle_request)
    page.goto(url)
    # time.sleep(1)
    cookies = context.cookies()
    result = {}
    for item in cookies:
        result[item['name']] = item['value']
    # 关闭页面
    page.close()
    return result
@app.route("/get-cookies", methods=["POST"])
def get_cookies():
    data = request.json
    url = data.get('url', '')
    html = data.get('html', '')
    user_agent = data.get('user_agent', '')
    cookies = generate_cookies(url, html, user_agent=user_agent)
    result = {}
    result['cookies'] = cookies
    return jsonify(result)
if __name__ == "__main__":
    app.run(host="0.0.0.0", threaded=False, processes=1, port=3000, debug=False)
```

测试代码

```
import requests
headers = {
    'Content-Type': 'application/json',
}
json_data = {
    'url': 'https://www.baidu.com',
    'html': '<html><head><title>Test Page</title></head><body><script>document.cookie = "test=123; path=/"; document.cookie = "user=testuser; path=/";</script></body></html>',
}
response = requests.post('http://localhost:3000/get-cookies', headers=headers, json=json_data)
print(response.status_code, response.text)
```

简简单单，有点意思。当然要运用到生产环境中，还需要解决很多问题，比如内存泄漏，性能等等。
代码都放在Github仓库https://github.com/dengshilong/browser_server里了，有兴趣的可以看看。

title: 用Locust测试接口性能
date: 2025-03-31 19:13:56
tags:
    - Python
    - 性能
categories:
---
通常我们写好一个接口后，需要做接口性能测试，知道接口的QPS(Queries Per Second)，百分位响应时间，我们可以用Python库Locust来做

pip install locust库后，新建locustfile.py，写入要测试的接口，demo如下

```
from locust import HttpUser, task, between
import json

class MyUser(HttpUser):
    # 设置用户的等待时间（模拟用户在操作之间的思考时间）
    wait_time = between(1, 2)  # 每次任务之间等待 1~2 秒

    @task
    def post_request(self):
        # 定义请求的 URL 和数据

        url = 'https://www.baidu.com'

        payload = {
            "url": url,
        }
        headers = {
            "Content-Type": "application/json"
        }

        # 发起 POST 请求
        with self.client.post('http://%s/api/generate_cookies' % '127.0.0.1:5009', json=payload, headers=headers, catch_response=True) as response:
            # 验证响应状态码是否为 200
            if response.status_code == 200:
                try:
                    # 如果需要验证返回内容，可以解析 JSON 数据
                    response.success()  # 标记请求成功
                except ValueError:
                    response.failure("Response is not valid JSON")
            else:
                # 如果状态码不是 200，标记请求失败
                response.failure(f"Status code: {response.status_code}")
```
 locust -f locustfile.py --web-port=8089，之后浏览器里打开 http://localhost:8089/ 就可以新建一个测试

测试结果中，RPS就是我们常说的QPS，95%ile 指的是 95百分位响应时间 (Percentile Response Times)，也就是95%的请求的响应时间不超过某个值。


title: Zabbix维护添加
date: 2017-06-06 19:07:55
tags:
    - Python
    - Zabbix
categories:
---
有些时候，需要通过Zabbix的[API](https://www.zabbix.com/documentation/3.0/manual/api/reference/maintenance/create)添加维护，挂起Zabbix的报警，简单的API调用如下


```
from zabbix_client import ZabbixServerProxy
zapi = ZabbixServerProxy("http://127.0.0.1/")
print zapi.user.login(user="test", password="password")
print zapi.host.get(output=['hostid', 'host'])
import time
params = {
    "name": "madfsdfsadsdfsdf",
    "active_since": int(time.time()),
    "active_till": int(time.time()) + 3600,
    "hostids": ["10109"],
    "timeperiods": [
        {
            "start_time": 64800,
            "period": 3600
        }
    ]
}
# print zapi.maintenance.create(**params)
params = {
    "hostids": ["10109"]
}
print zapi.maintenance.get(**params)

params = ('19',)
print zapi.maintenance.delete(*params)
```

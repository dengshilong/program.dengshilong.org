title: 修改MySQL引擎脚本
date: 2016-09-26 21:13:34
tags:
    - MySQL
    - MyISAM
    - InnoDB
categories:
---
此前，MySQL的默认引擎是MyISAM, 所以导致数据库里很多表都是MyISAM, 而MyISAM是表级锁，很容易引起性能问题。最近服务又被锁住了，原因依然是MyISAM的表级锁。于是将MyISAM引擎改为InnoDB。

之前运维同事写过一个脚本，直接拿来用就好。
[github地址](https://github.com/dengshilong/tools/blob/master/change_table_engine.sh)

```
#!/bin/bash

# 将 db_name 下引擎为 MyISAM 的表改为 InnoDB

# 以下变量按需修改
host_name=''
user_name='root'  #  root 或该用户有 root 同等级权限
password=''
db_name=''

tables=$(mysql -h${host_name} -u${user_name} -p${password} -e "SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_SCHEMA='${db_name}' AND ENGINE='MyISAM';")

for table in ${tables}
do
    if [ ${table} != 'TABLE_NAME' ]; then  # 排除标题
        echo ${table}
        mysql -h${host_name} -u${user_name} -p${password} -e "ALTER TABLE ${db_name}.${table} ENGINE='InnoDB';"
    fi
done
```

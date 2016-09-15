title: MySQL命令之status
date: 2016-09-15 10:49:06
tags:
    - MySQL
    - status
categories:
---
有时候想了解MySQL的版本号，运行状态等，此时status命令派上了用场

在mysql客户端里输入status命令，可以查看MySQL服务器的运行状态
```
mysql> status
--------------
mysql  Ver 14.14 Distrib 5.7.10, for osx10.11 (x86_64) using  EditLine wrapper

Connection id:          282
Current database:       blog
Current user:           root@localhost
SSL:                    Not in use
Current pager:          less
Using outfile:          ''
Using delimiter:        ;
Server version:         5.7.10 Homebrew
Protocol version:       10
Connection:             Localhost via UNIX socket
Server characterset:    utf8
Db     characterset:    utf8
Client characterset:    utf8
Conn.  characterset:    utf8
UNIX socket:            /tmp/mysql.sock
Uptime:                 29 days 18 hours 32 min 59 sec

Threads: 1  Questions: 8074  Slow queries: 0  Opens: 1592  Flush tables: 1  Open tables: 354  Queries per second avg: 0.003
```

而当你想查看MySQL的表运行状态时，可以执行show table status
```

mysql> show table status;
+-----------------------+--------+---------+------------+------+----------------+-------------+------------------+--------------+-----------+----------------+---------------------+---------------------+---------------------+--------------------+----------+----------------+---------+
| Name                  | Engine | Version | Row_format | Rows | Avg_row_length | Data_length | Max_data_length  | Index_length | Data_free | Auto_increment | Create_time         | Update_time         | Check_time          | Collation          | Checksum | Create_options | Comment |
+-----------------------+--------+---------+------------+------+----------------+-------------+------------------+--------------+-----------+----------------+---------------------+---------------------+---------------------+--------------------+----------+----------------+---------+
| wp_commentmeta        | MyISAM |      10 | Dynamic    |   25 |            207 |        5184 |  281474976710655 |        10240 |         0 |            827 | 2016-03-21 16:04:14 | 2016-03-21 16:04:14 | NULL                | utf8_general_ci    |     NULL |                |         |
| wp_comments           | MyISAM |      10 | Dynamic    |  129 |            558 |       72008 |  281474976710655 |        20480 |         0 |           1005 | 2016-03-21 16:20:21 | 2016-03-21 16:20:21 | 2016-03-21 16:20:21 | utf8_general_ci    |     NULL |                |         |
| wp_links              | MyISAM |      10 | Dynamic    |   13 |             97 |        1272 |  281474976710655 |         3072 |         0 |             25 | 2016-03-21 16:04:14 | 2016-03-21 16:04:15 | NULL                | utf8_general_ci    |     NULL |                |         |
| wp_options            | MyISAM |      10 | Dynamic    |  247 |           1451 |      364504 |  281474976710655 |        22528 |      6084 |          95575 | 2016-03-21 16:20:22 | 2016-06-21 17:46:41 | NULL                | utf8_general_ci    |     NULL |                |         |
| wp_postmeta           | MyISAM |      10 | Dynamic    |  952 |            116 |      111032 |  281474976710655 |        47104 |        76 |           2312 | 2016-03-21 16:04:14 | 2016-05-30 14:39:33 | NULL                | utf8_general_ci    |     NULL |                |         |
| wp_posts              | MyISAM |      10 | Dynamic    |  782 |           4397 |     3439132 |  281474976710655 |      1702912 |         0 |           1212 | 2016-03-21 16:20:21 | 2016-06-21 17:46:38 | 2016-03-21 16:20:22 | utf8_general_ci    |     NULL |                |         |
| wp_term_relationships | MyISAM |      10 | Fixed      |  620 |             21 |       13020 | 5910974510923775 |        31744 |         0 |           NULL | 2016-03-21 16:04:15 | 2016-05-30 14:00:52 | NULL                | utf8_general_ci    |     NULL |                |         |
| wp_term_taxonomy      | MyISAM |      10 | Dynamic    |  368 |             39 |       14696 |  281474976710655 |        17408 |         0 |            421 | 2016-03-21 16:04:15 | 2016-05-30 14:00:53 | NULL                | utf8_general_ci    |     NULL |                |         |
| wp_termmeta           | InnoDB |      10 | Dynamic    |    0 |              0 |       16384 |                0 |        32768 |         0 |              1 | 2016-07-04 11:14:31 | NULL                | NULL                | utf8mb4_unicode_ci |     NULL |                |         |
| wp_terms              | MyISAM |      10 | Dynamic    |  367 |             45 |       16880 |  281474976710655 |        35840 |         0 |            420 | 2016-03-21 16:04:15 | 2016-03-21 16:04:16 | NULL                | utf8_general_ci    |     NULL |                |         |
| wp_usermeta           | MyISAM |      10 | Dynamic    |   28 |             79 |        3092 |  281474976710655 |        10240 |       864 |             31 | 2016-03-21 16:04:15 | 2016-06-21 17:46:33 | NULL                | utf8_general_ci    |     NULL |                |         |
| wp_users              | MyISAM |      10 | Dynamic    |    1 |             96 |          96 |  281474976710655 |         4096 |         0 |              2 | 2016-03-21 16:20:21 | 2016-03-21 16:20:21 | NULL                | utf8_general_ci    |     NULL |                |         |
| wp_wp_rp_tags         | MyISAM |      10 | Dynamic    |  173 |             24 |        4200 |  281474976710655 |         8192 |         0 |           NULL | 2016-03-21 16:04:15 | 2016-03-21 16:04:16 | NULL                | latin1_swedish_ci  |     NULL |                |         |
+-----------------------+--------+---------+------------+------+----------------+-------------+------------------+--------------+-----------+----------------+---------------------+---------------------+---------------------+--------------------+----------+----------------+---------+
```

其中，Engine是使用的引擎，Row_format指的是行模式(Dynamic说明存在varchar字段, Fixed说明表的所有列长度都是固定的)，Rows指的是表记录数，Data_length指的是表数据大小。

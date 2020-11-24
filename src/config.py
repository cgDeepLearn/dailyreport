#!/usr/bin/env python
# -*- coding: utf-8 -*-

# redis queue
redis_host = '127.0.0.1'
redis_port = 6379
redis_pwd = 'test'
reids_db = 1

# db1数据库
db1_host = '127.0.0.1'
db1_port = 3306
db1_user = 'user1'
db1_pwd = 'pwd1'
db1_db = 'db1'

# db2数据库
db2_host = '127.0.0.1'
db2_port = 3306
db2_user = 'user2'
db2_pwd = 'pwd2'
db2_db = 'db2'

# 邮件配置
email_configs = {
    'email_to': 'basic',  # 基本邮件接收人,邮箱前缀
    'credit_emial_to': 'A,B',  # 报告其他接收人，邮箱前缀
    'report_days': 7,  # 多天汇总报告的天数，默认7天
    
}




#!/usr/bin/python
# coding:utf-8
#
# File Name: config.py
# File Author: lidey 
# File Created Date: 2015-11-27 17:31

import logging

# 服务配置信息
system = {
    'name': '大数据云--数据调度系统',
    'hostname': '10.211.55.2',
    'port': 8880,
    'company': '软通动力信息技术（集团）有限公司',
    'version': '0.0.1',
    'upload_file': '/Users/lidey/Documents/tmp/upload_file'
}

# 数据库配置
database = {
    'host': '10.211.55.15',
    # 'host': '127.0.0.1',
    'port': 3306,
    'database': 'cloud-data',
    'user': 'cloud-data',
    'password': 'cloud-data',
    # 'database': 'yxk',
    # 'user': 'root',
    # 'password': 'root',
    'max_connections': 3,
    'stale_timeout': 300,
    'charset': 'utf8',
}

# 缓存配置
redis = {
    'host': '10.211.55.15',
    'port': 6379,
    'db': 11,
}

# 日志配置
logger = {
    'level': logging.DEBUG
}


# spark配置
sparkConfig = {
    'startswith': 'com.memory',
    'upload_path': 'spark_jobs',
}

#!/usr/bin/python
# coding:utf-8
#
# File Name: config.py
# File Author: lidey 
# File Created Date: 2015-11-27 17:31

# 数据库配置信息
import logging

database = {
    # 'host': '10.211.55.15',
    'host': '127.0.0.1',
    'port': 3306,
    # 'database': 'cloud-data',
    # 'user': 'cloud-data',
    # 'password': 'cloud-data',
    'database': 'yxk',
    'user': 'root',
    'password': 'root',
    'max_connections': 10,
    'stale_timeout': 300,
    'charset': 'utf8',
}
redis = {
    'host': '10.211.55.15',
    'port': 6379,
    'db': 11,
}

logger = {
    'level': logging.DEBUG
}
# web服务配置信息
port = 8880

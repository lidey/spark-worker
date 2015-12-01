#!/usr/bin/python
# coding=utf-8
#
# File Name: router.py.py
# File Author: lidey 
# File Created Date: 2015-11-27 12:47
from app.handlers.job_handler import JobHandler
from app.handlers.user_handler import UserHandler
from app.handlers.index_handler import MainHandler

urls = [
    (r"/", MainHandler, dict()),
    (r"/user/(.*)", UserHandler, dict()),
    (r"/job/(.*)", JobHandler, dict()),
]

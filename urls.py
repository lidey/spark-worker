#!/usr/bin/python
# coding=utf-8
# 
# Filename: urls.py
# url路由表


import router
import app.core.router

urls = router.urls + app.core.router.urls

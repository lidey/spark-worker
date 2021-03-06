#!/usr/bin/python
# coding=utf-8
# Filename: application.py
import tornado.web
import os

import router
import app.router

settings = {
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/user/login",
    "xsrf_cookies": False,
    'debug': True,
}

application = tornado.web.Application(
        handlers=router.urls + app.router.urls,
        **settings
)

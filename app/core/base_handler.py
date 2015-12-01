#!/usr/bin/python
# coding=utf-8
#
# File Name: base.py
# File Author: lidey
# File Created Date: 2015-11-26 20:13
import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get_current_user(self):
        return self.get_secure_cookie("user")

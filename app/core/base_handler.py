#!/usr/bin/python
# coding=utf-8
#
# File Name: base.py
# File Author: lidey
# File Created Date: 2015-11-26 20:13
from datetime import datetime
from json import JSONDecoder
import json
from tornado.escape import utf8
from tornado.util import unicode_type
from json import JSONDecoder

import tornado.web


class BaseHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get_current_user(self):
        return self.get_secure_cookie("user")

    def prepare(self):
        args = dict()
        if self.request.body:
            try:
                args = JSONDecoder().decode(self.request.body)
            except ValueError:
                pass
        self.args = args

    def on_finish(self):
        self.set_cookie("_xsrf", self.xsrf_token)


    def prepare(self):
        args = dict()
        if self.request.body:
            try:
                args = JSONDecoder().decode(self.request.body)
            except ValueError:
                pass
        self.args = args

    def on_finish(self):
        self.set_cookie("_xsrf", self.xsrf_token)

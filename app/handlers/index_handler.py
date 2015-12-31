#!/usr/bin/python
# coding=utf-8
#
# File Name: index.py
# File Author: lidey
# File Created Date: 2015-11-26 20:13
import tornado.web
import tornado.escape
import os
from app.core.base_handler import BaseHandler
from config import system


class MainHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    @tornado.web.authenticated
    def get(self):
        routes = os.listdir(os.getcwd() + "/static/js/router")
        self.render('index.html', routes=routes, system=system, system_str=str(system))

    @tornado.web.authenticated
    def post(self):
        pass

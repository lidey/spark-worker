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


class MainHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    @tornado.web.authenticated
    def get(self, url_str=''):
        if url_str == '':
            self.index()

    @tornado.web.authenticated
    def post(self, url_str=''):
        if url_str == '':
            self.index()

    @tornado.web.authenticated
    def index(self):
        routes = os.listdir(os.getcwd() + "/static/js/router")
        self.render('index.html', routes=routes)

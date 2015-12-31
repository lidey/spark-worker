#!/usr/bin/python
# coding=utf-8
#
# File Name: index.py
# File Author: lidey
# File Created Date: 2015-11-26 20:13
import tornado.web
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
        name = tornado.escape.xhtml_escape(self.current_user)
        self.render('index.html', name=name)

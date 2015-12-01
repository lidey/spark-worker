#!/usr/bin/python
# coding=utf-8
#
# File Name: login.py
# File Author: lidey
# File Created Date: 2015-11-26 20:13

from app.core.base_handler import BaseHandler


class UserHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self, url_str=''):
        if url_str == '':
            return
        if url_str == 'login':
            self.to_login()

    def post(self, url_str=''):
        if url_str == '':
            return
        if url_str == 'login':
            self.login()

    def login(self):
        self.set_secure_cookie("user", self.get_argument("loginName"))
        self.redirect("/")

    def to_login(self):
        self.render('login.html')

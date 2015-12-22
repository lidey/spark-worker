#!/usr/bin/python
# coding=utf-8
#
# File Name: login.py
# File Author: lidey
# File Created Date: 2015-11-26 20:13
from peewee import DoesNotExist
from tornado import gen
from tornado import web
from tornado import escape

from app.core.base_handler import BaseHandler
from app.model.user_model import User


class UserHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    def get(self, url_str=''):
        if url_str == '':
            return
        if url_str == 'login':
            self.to_login()
        if url_str == 'logout':
            self.logout()
        if url_str == 'current':
            self.current()

    def post(self, url_str=''):
        if url_str == '':
            return
        if url_str == 'login':
            self.login()

    @web.asynchronous
    @gen.coroutine
    def login(self):
        user = User()
        user.login_name = str(self.get_argument("loginName"))
        user.password = str(self.get_argument("password"))
        if not user.login_name.strip() or not user.password.strip():
            self.render('login.html', msg='请输入的账号或密码.')
        hex = user.hex_password()
        try:
            user = User.get(User.login_name == user.login_name)
            if cmp(user.password, hex):
                self.set_secure_cookie("user", user.uuid)
                self.redirect("/")
            else:
                self.render('login.html', msg='您输入的密码错误.')
        except DoesNotExist:
            self.render('login.html', msg='您输入的账号信息错误.')

    def to_login(self):
        self.render('login.html', msg='')

    def logout(self):
        self.clear_all_cookies()
        self.redirect("/")

    def current(self):
        uuid = escape.xhtml_escape(self.current_user)
        user = User.get(User.uuid == uuid)
        self.write(user.to_dict())

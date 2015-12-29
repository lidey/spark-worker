#!/usr/bin/python
# coding=utf-8
#
# File Name: database_handler.py
# File Author: 姚丰利(lidey) 
# File Created Date: 2015-12-28 12:54
import tornado.web

from app.connect.connect_manager import DatabaseConnect
from app.core.base_exception import ConnectException
from app.core.base_handler import BaseHandler
from app.model.database_model import Database


class DatabaseHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    @tornado.web.authenticated
    def get(self, url_first='', url_second=''):
        if url_first == '':
            return
        if url_second == 'tables':
            self.tables(url_first)
        if url_second == 'columns':
            self.columns(url_first)

    @tornado.web.authenticated
    def get(self, url_first=''):
        if url_first == '':
            return
        if url_first == 'tree':
            self.tree()
        if url_first == 'test':
            self.test()

    def tree(self):
        tree = []
        for database in Database.select():
            tree.append(database.to_tree())
        self.write({'tree': tree})

    def tables(self, uuid):
        self.write({'tables': DatabaseConnect().get_tables(uuid, self.get_argument('name'))})

    def columns(self, uuid):
        self.write({'columns': DatabaseConnect().get_columns(uuid, self.get_argument('name'))})

    def test(self):
        try:
            DatabaseConnect().test(self.get_argument('uuid'))
            self.write({'success': True, 'content': '数据库测试成功'})
        except ConnectException, e:
            self.write({'success': False, 'content': '数据库测试失败,异常信息:<br/> {0}'.format(e.message)})

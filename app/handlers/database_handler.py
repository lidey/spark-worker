#!/usr/bin/python
# coding=utf-8
#
# File Name: database_handler.py
# File Author: 姚丰利(lidey) 
# File Created Date: 2015-12-28 12:54
import uuid
from datetime import datetime

import tornado.web

from app.connect.connect_manager import DatabaseConnect
from app.core.base_exception import ConnectException
from app.core.base_handler import BaseHandler
from app.model.database_model import Database, Folder


class DatabaseHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    @tornado.web.authenticated
    def post(self, url_first='', url_second=''):
        if url_first == '':
            return
        if url_first == 'save':
            database = Database()
            database.uuid = self.args.get('uuid')
            database.title = self.args.get('title')
            database.description = self.args.get('description')
            database.hostname = self.args.get('hostname')
            database.port = self.args.get('port')
            database.type = self.args.get('type')
            database.name = self.args.get('name')
            database.username = self.args.get('username')
            database.password = self.args.get('password')
            return self.save_database(database)
        if url_first == 'folder' and url_second == 'save':
            folder = Folder()
            folder.uuid = self.args.get('uuid')
            folder.db_uuid = self.args.get('db_uuid')
            folder.title = self.args.get('title')
            folder.description = self.args.get('description')
            return self.save_folder(folder)

    @tornado.web.authenticated
    def get(self, url_first='', url_second=''):
        if url_first == '':
            return
        if url_first == 'tree':
            return self.tree()
        if url_first == 'test':
            return self.test()
        if url_first == 'remove':
            return self.remove_database()
        if url_first == 'folder' and url_second == 'remove':
            return self.remove_folder()
        if url_second == 'tables':
            return self.tables(url_first)
        if url_second == 'columns':
            return self.columns(url_first)

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

    def save_database(self, database):
        if database.uuid is None:
            database.uuid = str(uuid.uuid1())
            database.save(force_insert=True)
        else:
            database.save()
        self.write({'success': True, 'content': '数据库链接保存成功.'})

    def save_folder(self, folder):
        if folder.uuid is None:
            folder.uuid = str(uuid.uuid1())
            folder.database = Database.get(Database.uuid == folder.db_uuid)
            folder.save(force_insert=True)
        else:
            folder.save()
        self.write({'success': True, 'content': '目录保存成功.'})

    def remove_database(self):
        Database.get(Database.uuid == self.get_argument('uuid')).delete_instance()
        self.write({'success': True, 'content': '数据库链接删除成功.'})

    def remove_folder(self):
        Folder.get(Folder.uuid == self.get_argument('uuid')).delete_instance()
        self.write({'success': True, 'content': '目录删除成功.'})

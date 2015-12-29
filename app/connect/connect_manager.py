#!/usr/bin/python
# coding=utf-8
#
# File Name: connect_manager.py
# File Author: 姚丰利(lidey) 
# File Created Date: 2015-12-28 11:40
from app.connect.mysql_connect import MysqlConnect
from app.model.database_model import Database

db_connects = {}


class DatabaseConnect:
    """
    数据连接管理类
    """

    def __init__(self):
        pass

    def init_all(self):
        """
        :return: 初始化全部数据库链接
        """
        for database in Database.select():
            db_connects[database.uuid] = self.connect(database)

    def connect(self, database):
        return {
            'mysql': lambda tmp: MysqlConnect(tmp),
        }[database.type](database)

    def reconnect(self):
        pass

    def get_cur(self, uuid):
        if not db_connects.has_key(uuid):
            database = Database.get(Database.uuid == uuid)
            db_connects[uuid] = self.connect(database)
        return db_connects[uuid]

    def get_tables(self, uuid, search):
        return self.get_cur(uuid).get_tables(search)

    def get_columns(self, uuid, table):
        return self.get_cur(uuid).get_columns(table)

    def test(self, uuid):
        self.get_cur(uuid).test()

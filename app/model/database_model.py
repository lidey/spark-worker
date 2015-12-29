#!/usr/bin/python
# coding=utf-8
#
# File Name: database_model.py
# File Author: 姚丰利(lidey) 
# File Created Date: 2015-12-28 11:46



# !/usr/bin/python
#
# File Name: user.py
# File Author: lidey
# File Created Date: 2015-11-26 20:13
import time
from peewee import *
from app.core.base_model import BaseModel
import hashlib


class Database(BaseModel):
    uuid = CharField(db_column='UUID', max_length=64, primary_key=True)
    title = CharField(db_column='TITLE', max_length=32)
    description = TextField(db_column='DESCRIPTION')
    hostname = CharField(db_column='HOST_NAME', max_length=15)
    port = IntegerField(db_column='PORT')
    name = CharField(db_column='NAME', max_length=32)
    username = CharField(db_column='USER_NAME', max_length=32)
    password = CharField(db_column='PASSWORD', max_length=32)
    type = CharField(db_column='TYPE_FLAG', max_length=16)
    created_time = DateTimeField(db_column='CREATED_DATE', null=False)
    delete_time = DateTimeField(db_column='DELETE_DATE', null=False)

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'title': self.title,
            'description': self.description,
            'hostname': self.hostname,
            'port': self.port,
            'username': self.username,
            'password': '',
            'type': self.type,
            'created_time': time.mktime(self.created_time.timetuple()) * 1000,
        }

    def to_tree(self):
        return {
            'uid': self.uuid,
            'label': self.title,
            'icon': ['fa', ' fa-database'],
            'type': 'database',
            'children': [{
                'uid': 'default',
                'label': '默认目录',
                'type': 'group',
                'icon': ['fa fa-folder-o'],
            }],
            'data': {
                'uuid': self.uuid,
                'title': self.title,
                'description': self.description,
                'hostname': self.hostname,
                'port': self.port,
                'name': self.name,
                'username': self.username,
                'password': '',
                'type': self.type,
                'created_time': time.mktime(self.created_time.timetuple()) * 1000,
            }
        }

    class Meta:
        db_table = 'WORKER_BI_DATABASE'

#
# class Table(BaseModel):
#     uuid = CharField(db_column='UUID', max_length=64, primary_key=True)
#     title = CharField(db_column='TITLE', max_length=32)
#     description = TextField(db_column='DESCRIPTION')
#     hostname = CharField(db_column='HOST_NAME', max_length=15)
#     port = IntegerField(db_column='PORT')
#     name = CharField(db_column='NAME', max_length=32)
#     username = CharField(db_column='USER_NAME', max_length=32)
#     password = CharField(db_column='PASSWORD', max_length=32)
#     type = CharField(db_column='TYPE_FLAG', max_length=16)
#     created_time = DateTimeField(db_column='CREATED_DATE', null=False)
#     delete_time = DateTimeField(db_column='DELETE_DATE', null=False)
#
#     def to_dict(self):
#         return {
#             'uuid': self.uuid,
#             'title': self.title,
#             'description': self.description,
#             'hostname': self.hostname,
#             'port': self.port,
#             'username': self.username,
#             'password': '',
#             'type': self.type,
#             'created_time': time.mktime(self.created_time.timetuple()) * 1000,
#         }
#
#     class Meta:
#         db_table = 'WORKER_BI_DATABASE'

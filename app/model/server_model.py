#!/usr/bin/python
# coding=utf-8
#
# File Name: server_model.py
# File Author: 姚丰利(lidey) 
# File Created Date: 2015-12-03 17:37
import time
from peewee import *
from app.core.base_model import BaseModel


class Folder(BaseModel):
    """
    链接分类目录
    """
    uuid = CharField(db_column='UUID', max_length=64, primary_key=True)
    title = CharField(db_column='TITLE', max_length=32)
    description = TextField(db_column='DESCRIPTION')
    created_time = DateTimeField(db_column='CREATED_DATE', null=False)

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'title': self.title,
            'description': self.description,
            'created_time': time.mktime(self.created_time.timetuple()) * 1000,
        }

    def to_tree(self):
        return {
            'uid': self.uuid,
            'label': self.title,
            'icon': ['fa fa-folder-o'],
            'type': 'folder',
            'data': {
                'uuid': self.uuid,
                'title': self.title,
                'description': self.description,
                'created_time': time.mktime(self.created_time.timetuple()) * 1000,
            }
        }

    class Meta:
        db_table = 'WORKER_SERVER_FOLDER'


class Server(BaseModel):
    """
    服务器链接
    """
    uuid = CharField(db_column='UUID', max_length=64, primary_key=True)
    folder = ForeignKeyField(Folder, db_column='FOLDER_UUID')
    title = CharField(db_column='TITLE', max_length=32)
    description = TextField(db_column='DESCRIPTION')
    host = CharField(db_column='HOST', max_length=32)
    version = CharField(db_column='VERSION_FLAG', max_length=32)
    type = CharField(db_column='TYPE_FLAG', max_length=32)
    name = CharField(db_column='NAME', max_length=64)
    password = CharField(db_column='PASSWORD', max_length=64)
    path = CharField(db_column='PATH', max_length=256)
    processor = IntegerField(db_column='PROCESSOR_NUM', default=0)
    memory = IntegerField(db_column='MEMORY', default=0)
    created_time = DateTimeField(db_column='CREATED_TIME', null=False)

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'title': self.title,
            'description': self.description,
            'host': self.host,
            'version': self.version,
            'type': self.type,
            'name': self.name,
            'password': self.password,
            'path': self.path,
            'processor': self.processor,
            'memory': self.memory,
            'created_time': time.mktime(self.created_time.timetuple()) * 1000,
        }

    class Meta:
        db_table = 'WORKER_SERVER_INFO'

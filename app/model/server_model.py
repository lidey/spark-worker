#!/usr/bin/python
# coding=utf-8
#
# File Name: server_model.py
# File Author: 姚丰利(lidey) 
# File Created Date: 2015-12-03 17:37
import time
import datetime
from peewee import *
from app.core.base_model import BaseModel


class Server(BaseModel):
    uuid = CharField(db_column='UUID', max_length=64, primary_key=True)
    title = CharField(db_column='TITLE', max_length=32)
    description = TextField(db_column='DESCRIPTION')
    host = CharField(db_column='HOST', max_length=32)
    version = CharField(db_column='VERSION_FLAG', max_length=32)
    name = CharField(db_column='NAME', max_length=64)
    password = CharField(db_column='PASSWORD', max_length=64)
    cpu = IntegerField(db_column='CPU_NUM', default=0)
    core = IntegerField(db_column='CORE_NUM', default=0)
    men = IntegerField(db_column='MEN_NUM', default=0)
    created_time = DateTimeField(db_column='CREATED_TIME', null=False)

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'title': self.title,
            'description': self.description,
            'host': self.host,
            'version': self.version,
            'name': self.name,
            'password': self.password,
            'cpu': self.cpu,
            'core': self.core,
            'men': self.men,
            'created_time': time.mktime(self.created_time.timetuple()) * 1000,
        }

    class Meta:
        db_table = 'WORKER_SERVER_INFO'
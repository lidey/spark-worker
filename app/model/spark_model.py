#!/usr/bin/python
# coding=utf-8
#
# File Name: server_model.py
# File Author: 姚丰利(lidey) 
# File Created Date: 2015-12-03 17:37
import time
from peewee import *
from app.core.base_model import BaseModel
from app.model.server_model import Server


class Spark(BaseModel):
    uuid = CharField(db_column='UUID', max_length=64, primary_key=True)
    server = ForeignKeyField(Server, db_column='SERVER_UUID')
    web_ui = CharField(db_column='WEB_UI', max_length=256)
    url = CharField(db_column='URL', max_length=236)
    rest_url = CharField(db_column='REST_URL', max_length=236)
    max_processor = IntegerField(db_column='MAX_PROCESSOR_NUM', default=10)
    max_memory = IntegerField(db_column='MAX_MEMORY', default=10240)
    path = CharField(db_column='PATH', max_length=256)
    created_time = DateTimeField(db_column='CREATED_TIME', null=False)

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'title': self.server.title,
            'description': self.server.description,
            'path': self.path,
            'url': self.url,
            'rest_url': self.rest_url,
            'web_ui': self.web_ui,
            'max_processor': self.max_processor,
            'max_memory': self.max_memory,
            'created_time': time.mktime(self.server.created_time.timetuple()) * 1000,
        }

    class Meta:
        db_table = 'WORKER_SERVER_SPARK'


class SparkJob(BaseModel):
    uuid = CharField(db_column='UUID', max_length=64, primary_key=True)
    spark = ForeignKeyField(Spark, db_column='SPARK_UUID')
    title = CharField(db_column='TITLE', max_length=32)
    description = TextField(db_column='DESCRIPTION')
    main_class = CharField(db_column='MAIN_CLASS', max_length=256)
    master = CharField(db_column='MASTER', max_length=236)
    arguments = CharField(db_column='ARGUMENTS', max_length=236)
    processor = IntegerField(db_column='PROCESSOR_NUM', default=10)
    memory = IntegerField(db_column='MEMORY', default=10240)
    created_time = DateTimeField(db_column='CREATED_TIME', null=False)

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'title': self.title,
            'description': self.description,
            'processor': self.processor,
            'memory': self.memory,
            'main_class': self.main_class,
            'master': self.master,
            'arguments': self.arguments,
            'created_time': time.mktime(self.created_time.timetuple()) * 1000,
        }

    class Meta:
        db_table = 'WORKER_SERVER_SPARK_JOB'

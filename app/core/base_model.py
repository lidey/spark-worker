#!/usr/bin/python
# coding=utf-8
#
# File Name: base_model.py
# File Author: lidey 
# File Created Date: 2015-11-27 17:29

# create a base model class that our application's models will extend. From django
import pymysql
from peewee import *
from playhouse import shortcuts
import config
from playhouse.pool import PooledMySQLDatabase

db = PooledMySQLDatabase(config.database['database'],
                         max_connections=config.database['max_connections'],
                         stale_timeout=config.database['stale_timeout'],
                         **{'host': config.database['host'],
                            'user': config.database['user'],
                            'password': config.database['password'],
                            'charset': config.database['charset']})


class BaseModel(Model):
    def __init__(self):
        super(BaseModel, self).__init__()

    def to_json(self):
        return shortcuts.model_to_dict(self)

    class Meta:
        database = db

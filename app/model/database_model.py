#!/usr/bin/python
# coding=utf-8
#
# File Name: database_model.py
# File Author: 姚丰利(lidey) 
# File Created Date: 2015-12-28 11:46
import time
from peewee import *
from app.core.base_model import BaseModel


class Database(BaseModel):
    """
    数据库链接
    """
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
        database = {
            'uid': self.uuid,
            'label': self.title,
            'icon': ['fa', ' fa-database'],
            'type': 'database',
            'children': list(),
            'data': {
                'uuid': self.uuid,
                'title': self.title,
                'description': self.description,
                'hostname': self.hostname,
                'port': self.port,
                'name': self.name,
                'username': self.username,
                'password': self.password,
                'type': self.type,
                'created_time': time.mktime(self.created_time.timetuple()) * 1000,
            }
        }
        database['children'].append({
            'uid': '{0}-default'.format(self.uuid),
            'label': '默认目录',
            'type': 'folder-default',
            'icon': ['fa fa-folder-o'],
            'data': {'db_uuid': self.uuid},
        })
        for folder in Folder.select().join(Database).where(Database.uuid == self.uuid):
            database['children'].append(folder.to_tree())
        return database

    class Meta:
        db_table = 'WORKER_DATABASE'


class Folder(BaseModel):
    """
    数据分类目录
    """
    uuid = CharField(db_column='UUID', max_length=64, primary_key=True)
    database = ForeignKeyField(Database, db_column='DATABASE_UUID')
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
                'db_uuid': self.database.uuid,
                'description': self.description,
                'created_time': time.mktime(self.created_time.timetuple()) * 1000,
            }
        }

    class Meta:
        db_table = 'WORKER_DATABASE_FOLDER'


class Table(BaseModel):
    """
    分类目录数据表
    """
    uuid = CharField(db_column='UUID', max_length=64, primary_key=True)  # 主键
    database = ForeignKeyField(Database, db_column='DATABASE_UUID', default=None)  # 数据库关联
    folder = ForeignKeyField(Folder, db_column='FOLDER_UUID')  # 分类目录关联
    name = CharField(db_column='NAME', max_length=32)  # 表名
    type = CharField(db_column='TYPE_FLAG', max_length=16)  # 类型
    created_time = DateTimeField(db_column='CREATED_DATE', null=False)  # 创建时间

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'name': self.name,
            'type': self.type,
            'created_time': time.mktime(self.created_time.timetuple()) * 1000,
        }

    class Meta:
        db_table = 'WORKER_DATABASE_TABLE'


class Column(BaseModel):
    """
    数据表 表结构
    """
    uuid = CharField(db_column='UUID', max_length=64, primary_key=True)
    database = ForeignKeyField(Database, db_column='DATABASE_UUID')
    table = ForeignKeyField(Table, db_column='TABLE_UUID')
    field = CharField(db_column='FIELD', max_length=32)
    type = CharField(db_column='TYPE_FLAG', max_length=16)
    key = CharField(db_column='KEY_FLAG', max_length=8)
    created_time = DateTimeField(db_column='CREATED_DATE', null=False)

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'field': self.field,
            'key': self.key,
            'type': self.type,
            'created_time': time.mktime(self.created_time.timetuple()) * 1000,
        }

    class Meta:
        db_table = 'WORKER_DATABASE_COLUMN'


class Category(BaseModel):
    """
    数据模型
    """
    uuid = CharField(db_column='UUID', max_length=64, primary_key=True)
    parent = ForeignKeyField('self', db_column='PARENT_UUID', default=None)
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
        group = {
            'uid': self.uuid,
            'label': self.title,
            'icon': ['fa', ' fa-cubes'],
            'type': 'category',
            'children': list(),
            'data': {
                'uuid': self.uuid,
                'title': self.title,
                'description': self.description,
                'created_time': time.mktime(self.created_time.timetuple()) * 1000,
            }
        }
        for child in self.select().where(Category.parent == self):
            group['children'].append(child.to_tree())
        return group

    class Meta:
        db_table = 'WORKER_DATABASE_MODEL_CATEGORY'


class Model(BaseModel):
    """
    数据模型
    """
    uuid = CharField(db_column='UUID', max_length=64, primary_key=True)
    database = ForeignKeyField(Database, db_column='DATABASE_UUID')
    category = ForeignKeyField(Category, db_column='CATEGORY_UUID')
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

    class Meta:
        db_table = 'WORKER_DATABASE_MODEL_INFO'

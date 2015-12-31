#!/usr/bin/python
#
# File Name: user.py
# File Author: lidey
# File Created Date: 2015-11-26 20:13
import time
from peewee import *
from app.core.base_model import BaseModel
import hashlib


class User(BaseModel):
    uuid = CharField(db_column='UUID', max_length=64, primary_key=True)
    login_name = CharField(db_column='LOGINNAME', max_length=32)
    password = CharField(db_column='USER_PASSWORD', max_length=64)
    img_url = CharField(db_column='IMG_URL', max_length=255)
    name = CharField(db_column='NAME', max_length=32)
    mail = CharField(db_column='E_MAIL', max_length=255)
    register_time = DateTimeField(db_column='REGISTER_DATE', null=False)

    def hex_password(self):
        return hashlib.sha1((self.login_name + '{' + self.password + '}').encode('utf-8')).hexdigest()

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'login_name': self.login_name,
            'password': '',
            'img_url': self.img_url,
            'name': self.name,
            'mail': self.mail,
            'register_time': time.mktime(self.register_time.timetuple()) * 1000,
        }

    class Meta:
        db_table = 'WORKER_USER_INFO'


class Setting(BaseModel):
    uuid = CharField(db_column='UUID', max_length=64, primary_key=True)
    user = ForeignKeyField(User, db_column='USER_UUID')
    theme_id = CharField(db_column='THEME_ID', max_length=64, default='1')
    header_fixed = CharField(db_column='HEADER_FIXED', max_length=8, default='true')
    aside_fixed = CharField(db_column='ASIDE_FIXED', max_length=8, default='false')
    aside_folded = CharField(db_column='ASIDE_FOLDED', max_length=8, default='false')
    aside_dock = CharField(db_column='ASIDE_DOCK', max_length=8, default='false')
    container = CharField(db_column='CONTAINER', max_length=8, default='false')
    navbar_header_color = CharField(db_column='NAVBAR_HEADER_COLOR', max_length=16, default='bg-black')
    navbar_collapse_color = CharField(db_column='NAVBAR_COLLAPSE_COLOR', max_length=16, default='bg-white-only')
    aside_color = CharField(db_column='ASIDE_COLOR', max_length=16, default='bg-black')
    created_time = DateTimeField(db_column='CREATED_TIME', null=False)

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'themeID': self.theme_id,
            'headerFixed': self.header_fixed == 'True',
            'asideFixed': self.aside_fixed == 'True',
            'asideFolded': self.aside_folded == 'True',
            'asideDock': self.aside_dock == 'True',
            'container': self.container == 'True',
            'navbarHeaderColor': self.navbar_header_color,
            'navbarCollapseColor': self.navbar_collapse_color,
            'asideColor': self.aside_color,
            'register_time': time.mktime(self.created_time.timetuple()) * 1000,
        }

    class Meta:
        db_table = 'WORKER_USER_SETTING'

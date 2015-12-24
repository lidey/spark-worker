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
    delete_time = DateTimeField(db_column='DELETE_DATE', null=False)

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

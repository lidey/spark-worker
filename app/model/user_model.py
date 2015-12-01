#!/usr/bin/python
#
# File Name: user.py
# File Author: lidey
# File Created Date: 2015-11-26 20:13
from peewee import *
from app.core.base_model import BaseModel


class User(BaseModel):
    uuid = CharField(db_column='UUID', max_length=64, primary_key=True)
    name = CharField(db_column='NAME', max_length=32)

    def find_uuid(self, uuid):
        return self.get(User.uuid == uuid)

    class Meta:
        db_table = 'M_USER'

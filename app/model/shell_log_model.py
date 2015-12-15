#!/usr/bin/python
# coding=utf-8
from peewee import *

from app.core.base_model import BaseModel
from app.model.script_model import Script


class ShellLog(BaseModel):
    uuid = CharField(db_column='UUID', max_length=64, primary_key=True)
    script_id = CharField(db_column='SCRIPT_ID', max_length=64)
    process_id = CharField(db_column='PROCESS_ID', max_length=64)
    log = TextField(db_column='LOG')
    status = IntegerField(db_column='STATUS')


    def find_uuid(self, uuid):
        return self.get(ShellLog.uuid == uuid)

    def to_dict(self):
        stat = ''
        if self.status == 1:
            stat = '成功'
        else:
            stat = '失败'

        script = Script().find_uuid(self.script_id)

        return {
            'id': self.uuid,
            'script': script.script,
            'script_title': script.title,
            'script_id': self.script_id,
            'status': stat,
            'log': self.log
        }
    class Meta:
        db_table = 'WORKER_SHELL_LOG'

#!/usr/bin/python
# coding=utf-8

from peewee import *
import time
from app.core.base_model import BaseModel


class Scheduler(BaseModel):
    uuid = CharField(db_column='UUID', max_length='64', primary_key='true')
    name = CharField(db_column='NAME', max_length='128') #调度器名称
    cron = CharField(db_column='CRON', max_length='128') #执行时间表达式
    jobId = CharField(db_column='JOBID', max_length='64') #调度的job的id
    status = IntegerField(db_column='STATUS')    #执行状态 0未执行 1启动 #2暂停
    msg = TextField(db_column='MSG')  #详细信息
    created_time = DateTimeField(db_column='CREATED_TIME', null='false')

    def to_dict(self):
        # stat = ''
        # if self.status == 0:
        #     stat = '未启动'
        # elif self.status == 1:
        #     stat = '启动'
        # elif self.status == 2:
        #     stat = '暂停'
        return {
            'uuid': self.uuid,
            'name': self.name,
            'cron': self.cron,
            'msg': self.msg,
            'status': self.status,
            'jobId': self.jobId,
            'created_time': time.mktime(self.created_time.timetuple()) * 1000,
        }

    def find_uuid(self, uuid):
        return self.get(Scheduler.uuid == uuid)


    def delete_uuid(self):
        self.delete_instance()

    class Meta:
        db_table = 'WORKER_SCHEDULER'

#!/usr/bin/python
# coding=utf-8
import time

from peewee import *
from app.core.base_model import BaseModel


class SchedulerCron(BaseModel):
    uuid = CharField(db_column='UUID', max_length=64, primary_key=True)
    second = CharField(db_column='SECOND_FLAG', max_length=16)
    minute = CharField(db_column='MINUTE_FLAG', max_length=16)
    hour = CharField(db_column='HOUR_FLAG', max_length=16)
    day = CharField(db_column='DAY_FLAG', max_length=16)
    month = CharField(db_column='MONTH_FLAG', max_length=16)
    week = CharField(db_column='WEEK_FLAG', max_length=16)
    year = CharField(db_column='YEAR_FLAG', max_length=16)
    created_time = DateTimeField(db_column='CREATED_TIME', null=False)

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'second': self.second,
            'minute': self.minute,
            'hour': self.hour,
            'day': self.day,
            'month': self.month,
            'week': self.week,
            'year': self.year,
            'created_time': time.mktime(self.created_time.timetuple()) * 1000,
        }

    class Meta:
        db_table = 'WORKER_SCHEDULER_CRON'


class Scheduler(BaseModel):
    uuid = CharField(db_column='UUID', max_length='64', primary_key='true')
    cron = ForeignKeyField(SchedulerCron, db_column='CRON_UUID')
    type = CharField(db_column='TYPE_FLAG', max_length='16')  # 执行状态 0未执行 1启动 #2暂停
    job_uuid = CharField(db_column='JOB_UUID', max_length='64')  # 调度的job的id
    title = CharField(db_column='TITLE', max_length='32')  # 调度器名称
    description = TextField(db_column='DESCRIPTION')  # 调度器名称
    status = CharField(db_column='STATUS_FLAG', max_length='16')  # 执行状态 0未执行 1启动 #2暂停
    created_time = DateTimeField(db_column='CREATED_TIME', null=False)

    def to_dict(self):
        scheduler = {
            'uuid': self.uuid,
            'job_uuid': self.job_uuid,
            'type': self.type,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'created_time': time.mktime(self.created_time.timetuple()) * 1000,
        }
        try:
            if self.cron.uuid is not None:
                scheduler['cron'] = self.cron.to_dict()
        except SchedulerCron.DoesNotExist:
            pass

        return scheduler

    class Meta:
        db_table = 'WORKER_SCHEDULER'


class SchedulerLog(BaseModel):
    uuid = CharField(db_column='UUID', max_length=64, primary_key=True)
    scheduler = ForeignKeyField(Scheduler, db_column='SCHEDULER_UUID')
    code = IntegerField(db_column='CODE_FLAG')
    status = CharField(db_column='STATUS_FLAG', max_length=16)
    std_err = TextField(db_column='STD_ERR')
    created_time = DateTimeField(db_column='CREATED_TIME', null=False)

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'scheduler': self.scheduler.to_dict(),
            'status': self.status,
            'code': self.code,
            'created_time': time.mktime(self.created_time.timetuple()) * 1000,
        }

    class Meta:
        db_table = 'WORKER_SCHEDULER_LOG'

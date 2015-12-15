#!/usr/bin/python
# coding=utf-8
import time
from peewee import *
from app.core.base_model import BaseModel
from app.model.job_model import Job


class JobProgress(BaseModel):
    uuid = CharField(db_column='UUID', max_length=64, primary_key=True)
    job_id = CharField(db_column='JOB_ID', max_length=64)      #任务id
    max_num = IntegerField(db_column='MAX_NUM')  #脚本总数
    success_num = IntegerField(db_column='SUCCESS_NUM')          #成功数量
    fail_num = IntegerField(db_column='FAIL_NUM')           #失败数量
    status = IntegerField(db_column='STATUS')    #执行状态 0 未执行 1正在执行  2 执行完成
    result = IntegerField(db_column='RESULT')   #执行结果 1 成功  2 失败
    startTime = DateTimeField(db_column='START_TIME')        #开始时间
    endTime = DateTimeField(db_column='END_TIME')            #结束时间

    def find_uuid(self, uuid):
        return self.get(JobProgress.uuid == uuid)

    def delete_uuid(self):
        self.delete_instance()

    def to_dict(self):
        stat = ""
        res = ""
        endDate = ''
        startDate = ''
        if self.status == 0:
            stat = "未执行"
        elif self.status == 1:
            stat = "正在执行"
        elif self.status == 2:
            stat = "执行完成"

        if self.result == 1:
            res = "成功"
        elif self.result == 2:
            res = "失败"
        if self.endTime:
            endDate = time.mktime(self.endTime.timetuple())*1000
        if self.startTime:
            startDate = time.mktime(self.startTime.timetuple())*1000
        job = Job().find_uuid(self.job_id)
        return {
            'job_title': job.title,
            'job_desc': job.desc,
            'status':  stat,
            'result': res,
            'startTime': startDate,
            'endTime': endDate,
            'id': self.uuid,
            'max_num': self.max_num,
            'fail_num': self.fail_num,
            'success_num': self.success_num,
            'job_id': self.job_id
        }
    class Meta:
        db_table = 'WORKER_JOB_PROGRESS'


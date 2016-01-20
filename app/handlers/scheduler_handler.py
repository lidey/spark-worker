#!/usr/bin/python
# coding=utf-8

import tornado.web
import uuid

from apscheduler.jobstores.base import JobLookupError
from peewee import JOIN

from app.core.base_handler import BaseHandler
from app.core.base_model import db
from app.model.scheduler_model import Scheduler, SchedulerCron, SchedulerLog
from app.model.spark_model import SparkJob
from app.scheduler.cron_scheduler import SchedulerEngine


class SchedulerHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    @tornado.web.authenticated
    def get(self, url_str=''):
        if url_str == '':
            return
        if url_str == 'list':
            self.list()
        if url_str == 'info':
            self.info()
        if url_str == 'delete':
            self.delete()
        if url_str == 'startup':
            self.startup()
        if url_str == 'shutdown':
            self.shutdown()
        if url_str == 'log_list':
            self.log_list()
        if url_str == 'log':
            self.log_info()

    @tornado.web.authenticated
    def post(self, url_str=''):
        if url_str == '':
            return
        if url_str == 'save':
            scheduler = Scheduler()
            scheduler.uuid = self.args.get("uuid")
            scheduler.type = self.args.get("type")
            scheduler.job_uuid = self.args.get("job_uuid")
            scheduler.description = self.args.get("description")
            scheduler.title = self.args.get("title")
            self.save(scheduler)
        if url_str == 'set_cron':
            cron = SchedulerCron()
            cron.uuid = self.args.get("uuid")
            cron.s_uuid = self.args.get("s_uuid")
            cron.second = self.args.get("second")
            cron.minute = self.args.get("minute")
            cron.hour = self.args.get("hour")
            cron.day = self.args.get("day")
            cron.month = self.args.get("month")
            cron.week = self.args.get("week")
            cron.year = self.args.get("year")
            self.set_cron(cron)

    def list(self):
        """
        获取调度任务列表
        :return:
        """
        schedulers = []
        for scheduler in Scheduler.select(Scheduler, SchedulerCron).join(SchedulerCron, JOIN.LEFT_OUTER):
            schedulers.append(scheduler.to_dict())
        self.write({"schedulers": schedulers})

    def log_list(self):
        """
        获取调度任务列表
        :return:
        """
        logs = []
        for log in SchedulerLog.select(SchedulerLog, Scheduler).join(Scheduler, JOIN.LEFT_OUTER):
            logs.append(log.to_dict())
        self.write({"logs": logs})

    @db.commit_on_success
    def delete(self):
        """
        删除调度任务
        :return:
        """
        try:
            scheduler = Scheduler.get(self.args.get("uuid"))
            SchedulerLog.delete().where(SchedulerLog.scheduler == scheduler).execute()
            scheduler.cron.delete_instance()
            scheduler.delete_instance()
            self.write({'success': True, 'content': '调度任务删除成功'})
        except Exception, e:
            self.write({'success': False, 'content': '调度任务删除失败'})
            print Exception, ':', e

    @db.commit_on_success
    def save(self, scheduler):
        """
        保存调度任务信息
        :param scheduler: 调度任务信息
        :return:
        """
        try:
            if scheduler.uuid is None:
                scheduler.uuid = str(uuid.uuid1())
                scheduler.status = 'DISABLE'
                scheduler.save(force_insert=True)
            else:
                scheduler.save()
            self.write({'success': True, 'content': '保存成功'})
        except Exception, e:
            self.write({'success': False, 'content': '保存失败'})
            print Exception, ':', e

    @db.commit_on_success
    def set_cron(self, cron):
        """
        设置调度规则
        :param cron:
        :return:
        """
        try:
            if cron.uuid is None:
                cron.uuid = str(uuid.uuid1())
                cron.save(force_insert=True)
                scheduler = Scheduler.get(Scheduler.uuid == cron.s_uuid)
                scheduler.cron = cron
                scheduler.save()
            else:
                cron.save()
                scheduler = Scheduler.select(Scheduler, SchedulerCron).join(SchedulerCron).where(
                        SchedulerCron.uuid == cron.uuid).get()
                if scheduler.status == 'ENABLE':
                    SchedulerEngine(Scheduler).reset()
            self.write({'success': True, 'content': '调度任务保存成功'})
        except Exception, e:
            self.write({'success': False, 'content': '调度任务保存失败'})
            print Exception, ':', e

    def info(self):
        """
        获取调度任务信息
        :return:
        """
        scheduler = Scheduler.get(Scheduler.uuid == self.get_argument("uuid"))
        scheduler_dict = scheduler.to_dict()
        if scheduler.type == 'SPARK':
            scheduler_dict['job'] = SparkJob.get(SparkJob.uuid == scheduler.job_uuid).to_dict()
        self.write(scheduler_dict)

    def log_info(self):
        """
        获取调度任务日志
        :return:
        """
        log = SchedulerLog.get(SchedulerLog.uuid == self.get_argument("uuid"))
        log_dict = log.to_dict()
        log_dict['std_err'] = log.std_err
        self.write(log_dict)

    @db.commit_on_success
    def startup(self):
        """
        执行调度任务
        :return:
        """
        try:
            scheduler = Scheduler.get(Scheduler.uuid == self.get_argument('uuid'))

            SchedulerEngine(scheduler).add()
            scheduler.status = 'ENABLE'
            scheduler.save()
            self.write({'success': True, 'content': '启用调度任务成功'})
        except Exception, e:
            self.write({'success': False, 'content': '启用调度任务出现异常'})
            print Exception, ':', e

    @db.commit_on_success
    def shutdown(self):
        """
        终止调度任务
        :return:
        """
        scheduler = Scheduler.get(Scheduler.uuid == self.get_argument('uuid'))
        try:
            SchedulerEngine(scheduler).remove()
            scheduler.status = 'DISABLE'
            scheduler.save()
        except JobLookupError, e:
            scheduler.status = 'DISABLE'
            scheduler.save()
            print e
        self.write({'success': True, 'content': '停用调度任务成功'})

#!/usr/bin/python
# coding=utf-8
#
# File Name: shell_scheduler.py
# File Author: 姚丰利(lidey) 
# File Created Date: 2015-11-29 21:47
import uuid

from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR, EVENT_JOB_MISSED

from app.core.base_model import db
from app.core.base_scheduler import scheduler
from app.model.scheduler_model import Scheduler, SchedulerCron, SchedulerLog
from app.script.spark_thread import startup_spark_job


class SchedulerEngine:
    """
    调度器核心任务程序
    """

    def __init__(self, scheduler):
        self.scheduler = scheduler
        self.cron = scheduler.cron

    def add(self):
        """
        添加调度任务
        :return:
        """
        if self.scheduler.type == 'SPARK':
            self._cron_add(startup_spark_job)

    def reset(self):
        """
        重置调度规则
        :return:
        """
        scheduler.reschedule_job(self.scheduler.uuid, trigger='cron', year=self.cron.year, week=self.cron.week,
                                 month=self.cron.month,
                                 day=self.cron.day,
                                 hour=self.cron.hour, minute=self.cron.minute, second=self.cron.second)

    def remove(self):
        """
        移除调度任务
        :return:
        """
        scheduler.remove_job(self.scheduler.uuid)

    def _cron_add(self, fun):
        """
        设置调度规则
        :return:
        """
        scheduler.add_job(fun, 'cron', year=self.cron.year, week=self.cron.week, month=self.cron.month,
                          day=self.cron.day,
                          hour=self.cron.hour, minute=self.cron.minute, second=self.cron.second,
                          id=self.scheduler.uuid, args=[self.scheduler.job_uuid])


def startup_enable_scheduler():
    """
    初始化启动中的项目
    :return:
    """
    for run in Scheduler.select(Scheduler, SchedulerCron).join(SchedulerCron).where(Scheduler.status == 'ENABLE'):
        SchedulerEngine(run).add()
    db.close()


def event_listener(event):
    """
    添加异常过滤器
    :param event:
    :return:
    """
    if not event.job_id.startswith('system-'):
        try:
            log = SchedulerLog()
            log.uuid = str(uuid.uuid1())
            log.scheduler = Scheduler.get(Scheduler.uuid == event.job_id)
            log.code = event.code
            if event.exception:
                log.status = 'ERROR'
                log.std_err = event.exception.message
            else:
                log.status = 'SUCCESS'
            log.created_time = event.scheduled_run_time
            log.save(force_insert=True)
        except Scheduler.DoesNotExist:
            pass
        finally:
            db.close()


scheduler.add_listener(event_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR | EVENT_JOB_MISSED)

startup_enable_scheduler()

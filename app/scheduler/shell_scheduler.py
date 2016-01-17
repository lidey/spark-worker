#!/usr/bin/python
# coding=utf-8
#
# File Name: shell_scheduler.py
# File Author: 姚丰利(lidey) 
# File Created Date: 2015-11-29 21:47
import datetime

from app.core.base_scheduler import scheduler
from app.model.user_model import User
from app.script.job_thread import JobThread


def tick(name):
    entity = User().find_uuid('asdas').to_json()
    print('%s say : The time is: %s. %s' % (name, datetime.datetime.now(), entity))


def run(job_uuid):
    JobThread(job_uuid);


class ShellScheduler:
    def __init__(self):
        pass

    def add_job(self, uuid, name):
        scheduler.add_job(tick, 'interval', seconds=3, id=uuid, args=[name])

    def remove_job(self, uuid):
        scheduler.remove_job(uuid)

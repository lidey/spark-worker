#!/usr/bin/python
# coding=utf-8
#
# File Name: shell_scheduler.py
# File Author: 姚丰利(lidey) 
# File Created Date: 2015-11-29 21:47
import datetime
from apscheduler.schedulers.tornado import TornadoScheduler

import config
from app.model.user_model import User

scheduler = TornadoScheduler({
    'apscheduler.executors.default': {
        'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
        'max_workers': '20'
    },
    'apscheduler.executors.processpool': {
        'type': 'processpool',
        'max_workers': '5'
    },
    'apscheduler.job_defaults.coalesce': 'false',
    'apscheduler.job_defaults.max_instances': '3',
    'apscheduler.timezone': 'UTC',
})
# scheduler.add_jobstore('redis', jobs_key='scheduler.jobs', run_times_key='scheduler.run_times',
#                        **{'host': config.redis['host'], 'port': config.redis['port'], 'db': config.redis['db']})
scheduler.start()


def tick(name):
    entity = User().find_uuid('asdas').to_json()
    print('%s say : The time is: %s. %s' % (name, datetime.datetime.now(), entity))


class ShellScheduler:
    def __init__(self):
        pass

    def add_job(self, uuid, name):
        scheduler.add_job(tick, 'interval', seconds=3, id=uuid, args=[name])

    def remove_job(self, uuid):
        scheduler.remove_job(uuid)

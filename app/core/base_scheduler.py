#!/usr/bin/python
# coding=utf-8
#
# File Name: shell_scheduler.py
# File Author: 姚丰利(lidey) 
# File Created Date: 2015-11-29 21:47
from apscheduler.schedulers.tornado import TornadoScheduler

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

# #!/usr/bin/python
# # coding=utf-8
#
# from apscheduler.schedulers.background import BlockingScheduler
# import datetime
# import os
#
# scheduler = BlockingScheduler({
#     'apscheduler.executors.default': {
#         'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
#         'max_workers': '20'
#     },
#     'apscheduler.executors.processpool': {
#         'type': 'processpool',
#         'max_workers': '5'
#     },
#     'apscheduler.job_defaults.coalesce': 'false',
#     'apscheduler.job_defaults.max_instances': '3',
#     'apscheduler.timezone': 'UTC',
# })
# def run():
#      print('Tick! The time is: %s' % datetime.now())
#
#
# class schedulerRun:
#
#     def add_job(self):
#         scheduler = BlockingScheduler()
#         try:
#             scheduler.add_job(run,'cron', second='*/3', hour='*')
#             print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
#             # scheduler.start()
#          except (KeyboardInterrupt, SystemExit):
#             scheduler.shutdown()
#
#
#
#

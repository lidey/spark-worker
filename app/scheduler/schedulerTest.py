# coding=utf-8
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.tornado import TornadoScheduler
from app.core.tools import get_uuid
from app.model.job_progress_model import JobProgress
from app.model.script_model import Script
from app.scheduler.method import runMethod
from app.script.thread import Thread
from datetime import datetime
import time
import os


def tick(name):
    print('Tick! The time is: %s' % datetime.now()+name)

# if __name__ == '__main__':
# scheduler = BlockingScheduler()
scheduler = BlockingScheduler({

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


def runJob(job_uuid):
    #查询job下所有的脚本
    #job_id = self.args.get("job_id")
    list = Script.select().where(Script.job_id == job_uuid)
    max_num = len(list);
    pro = JobProgress()
    pro.uuid = get_uuid()
    pro.job_id = job_uuid
    pro.max_num = max_num
    pro.success_num = 0;
    pro.fail_num = 0;
    pro.status = 0;
    pro.result = -1;
    pro.save(force_insert=True)
    #开启线程执行脚本 并保存执行记录
    #for i in list:
    Thread(pro.uuid);


class RunSchTest:
    def add_job(self, second, hour, uuid, name):

        r = runMethod();
        scheduler.add_job(r.doing, 'cron', second=second, hour=hour, id=uuid, name=name)
        print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()

    def remove_job(self, uuid):
        scheduler.remove_job(self, uuid)
        #scheduler.remove_all_jobs(self);
        print("finish?")


    def runJob(self, jobId, second):
        scheduler.add_job(runJob(jobId), 'cron', second=second)
        print("job running。。。")
        try:
            scheduler.start()
        except Exception, e:
            print Exception, ':', e


    # @scheduler.scheduled_job('cron', id='my_job_id', day='last sun')
    # def runTest(self):
    #     print("I am printed at 00:00:00 on the last Sunday of every month!")

    def runTest(self, name, second):
        #r = runMethod();r.tick
        scheduler.add_job(tick, [name], 'cron', second=second)
        print("runTesting...")
        try:
            scheduler.start()
        except Exception, e:
            print Exception, ':', e
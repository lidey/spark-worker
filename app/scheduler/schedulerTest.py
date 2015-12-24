# coding=utf-8
#from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.tornado import TornadoScheduler
from tornado.ioloop import IOLoop
from app.core.tools import get_uuid
from app.model.job_progress_model import JobProgress
from app.model.script_model import Script
from app.scheduler.method import runMethod
from app.script.job_thread import JobThread
from datetime import datetime
import time
import os


def tick():
    print('Tick! The time is: %s' % datetime.now()+test+'f u very much')

# if __name__ == '__main__':
# scheduler = BlockingScheduler()
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


def runJob():
    #查询job下所有的脚本
    #job_id = self.args.get("job_id")
    #print(">>>>>>>>>>>>>>>>>>>runDefRunJob<<<<<<<<<<<<<<<<<<<<")
    for job_uuid in jobIdArrayG:
        #print(">>>>>>>>>>>>>>>>>>>for<<<<<<<<<<<<<<<<<<<<")
        print job_uuid
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
        JobThread(pro.uuid);


jobIdArrayG = []
test = ''

class RunSchTest:
    def add_job(self, second, hour, uuid, name):

        r = runMethod();
        scheduler.add_job(r.doing, 'cron', seconds=second, hour=hour, id=uuid, name=name)
        print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()

    def remove_job(self, uuid):
        scheduler.remove_job(self, uuid)
        #scheduler.remove_all_jobs(self);
        print("finish?")


    def runJob1(self, jobId, second):
        scheduler.add_job(runJob(jobId), 'cron', seconds=second)
        print("job running。。。")
        try:
            scheduler.start()
        except Exception, e:
            print Exception, ':', e


    # @scheduler.scheduled_job('cron', id='my_job_id', day='last sun')
    # def runTest(self):
    #     print("I am printed at 00:00:00 on the last Sunday of every month!")

    def runing(self, jobIds, second, schedulerUUID):
        global jobIdArrayG
        jobIdArrayG = jobIds.split(',')
        # for jobId in jobIdArrayG:
        #     print jobId
        #r = runMethod();r.tick
        print(">>>>>>>>>>>>>>>>>>>runTest<<<<<<<<<<<<<<<<<<<<")
        scheduler.add_job(runJob, 'cron',  second=int(second), id=schedulerUUID)
        print("runTesting...")
        try:
            scheduler.start()
            IOLoop.instance().start()
        except Exception, e:
            print Exception, ':', e

    def runTest2(self, name, second, uuid, minute):
        global test
        test = name
        #r = runMethod();r.tick
        job = scheduler.add_job(tick, 'interval', id=uuid, seconds=second, minutes = minute)
        #scheduler.add_job(tick, 'interval', id=uuid, trigger='*/1 * * * *')
        print("runTesting...")
        try:
            scheduler.start()
            IOLoop.instance().start()
        except Exception, e:
            print Exception, ':', e

    def removeJobTest(self,uuid):
        scheduler.remove_job(uuid)


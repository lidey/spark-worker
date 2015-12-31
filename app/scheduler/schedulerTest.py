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

#测试方法
def tick():
    print('Tick! The time is: %s' % datetime.now()+test+'f u very much')

#定时job任务方法
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

#全局变量
jobIdArrayG = []
test = ''

class RunSchTest:

    def runing(self, jobIds, second, schedulerUUID):
        global jobIdArrayG
        jobIdArrayG = jobIds.split(',')
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

    def removeJob(self, uuid):
        scheduler.remove_job(uuid)


    def cronTest(self, year, month, day, week, day_of_week, hour, minute, second):
        scheduler.add_job(tick, 'cron', minute=minute, second=second)
        #scheduler.add_job(tick, 'cron', timezone='30 21 * * *')
        print("runTesting...")
        try:
            scheduler.start()
            IOLoop.instance().start()
        except Exception, e:
            print Exception, ':', e

    def runingJobs(self, jobIds, cron, schedulerUUID):
        global jobIdArrayG
        jobIdArrayG = jobIds.split(',')#处理jobId，放到全局数组变量中
        cronArray = [] #前台传来的表达式数组
        cronArray = cron.split(' ')
        #trigger = '' #那种类型的表达式 包括 cron interval date
        #year = '' #年
        week = '' #周
        month = '' #月
        day = '' #日
        hour = '' #小时
        minute = '' #分钟
        second = '' #秒
        #second = cronArray[5]
        #print 'second:'+second
        week = cronArray[4]
        month = cronArray[3]
        day = cronArray[2]
        hour = cronArray[1]
        minute = cronArray[0]
        scheduler.add_job(runJob, 'cron', month=month, week=week, day=day, hour=hour, minute=minute, id=schedulerUUID)
        try:
            scheduler.start()
            IOLoop.instance().start()
        except Exception, e:
            print Exception, ':', e
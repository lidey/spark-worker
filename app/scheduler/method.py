# coding=utf-8
from datetime import datetime
from app.core.tools import get_uuid
from app.model.job_progress_model import JobProgress
from app.model.script_model import Script
from app.script.job_thread import JobThread


class runMethod:
    # def __init__(self):
    #     print ("init f u ")

    def doing(self):
        print("f u very much")

    def tick(self):
        print('Tick! The time is: %s' % datetime.now())

    def runJob(self, jobId):
        # 查询job下所有的脚本
        # job_id = self.args.get("job_id")
        list = Script.select().where(Script.job_id == jobId)
        max_num = len(list);
        pro = JobProgress()
        pro.uuid = get_uuid()
        pro.job_id = jobId
        pro.max_num = max_num
        pro.success_num = 0;
        pro.fail_num = 0;
        pro.status = 0;
        pro.result = -1;
        pro.save(force_insert=True)

        # 开启线程执行脚本 并保存执行记录
        # for i in list:
        JobThread(pro.uuid);

    def tick(self, name):
        print('Tick! The time is: %s' % datetime.now() + name)

#!/usr/bin/python
# coding=utf-8

import threading
import datetime
from app.core.tools import get_uuid
from app.model.job_progress_model import JobProgress
from app.model.script_model import Script
from app.model.server_model import Server
from app.model.shell_log_model import ShellLog
from app.script.server_script import ServerScript


class Thread(threading.Thread):
    process_id = ""
    success = 0;
    fail = 0;
    def __init__(self, process_id):
        threading.Thread.__init__(self)
        self.process_id = process_id
        self.start();

    def run(self):
        pro = JobProgress.get(JobProgress.uuid == self.process_id)
        list = Script.select().where(Script.job_id == pro.job_id)
        pro.startTime = datetime.datetime.now()
        pro.save();
        for obj in list:
            job_progress = JobProgress.get(JobProgress.uuid == self.process_id)
            script = obj;
            host = Server.get(Server.uuid == script.server_id)
            server = ServerScript(host)
            success = job_progress.success_num;
            fail = job_progress.fail_num;
            try:
                out, err = server.command(script.script)  # 执行脚本
                if len(err) == 0:
                    # 执行成功
                    shell_log = ShellLog()
                    shell_log.script_id = obj.uuid
                    shell_log.process_id = self.process_id
                    shell_log.log = out
                    shell_log.uuid = get_uuid()
                    shell_log.status = 1

                    shell_log.save(force_insert=True)
                    print('执行成功前状态%d'%( job_progress.status))
                    print('执行成功前%d'%( job_progress.success_num))
                    success = job_progress.success_num + 1
                    print('执行成功后%d'%(success))
                else:
                    # 执行失败
                    shell_log = ShellLog()
                    shell_log.script_id = obj.uuid
                    shell_log.process_id = self.process_id
                    shell_log.log = out
                    shell_log.uuid = get_uuid()
                    shell_log.status = 2
                    shell_log.save(force_insert=True)
                    fail = job_progress.fail_num + 1

                num = job_progress.max_num


                 # 更新进程
                if num == success + fail:
                    job_progress.status = 2  # 执行完成
                    job_progress.endTime = datetime.datetime.now()
                else:
                    job_progress.status = 1  # 正在执行
                # 更新执行结果
                if job_progress.status == 2 and fail == 0:
                    job_progress.result = 1  # 成功
                elif job_progress.status == 2 and fail > 0:
                    job_progress.result = 2  # 失败

                job_progress.success_num = success;
                job_progress.fail_num = fail;
                print('执行数量成功%d,失败%d'%( success, fail))

                job_progress.save()

            except Exception, e:
                print Exception, e;  # 异常捕获

#!/usr/bin/python
# coding=utf-8
from tornado import gen

import tornado.web
import tornado.websocket
from app.core.base_handler import BaseHandler
from app.core.base_model import db
from app.core.tools import get_uuid
from app.model.job_progress_model import JobProgress
from app.model.script_model import Script
from app.model.shell_log_model import ShellLog
from app.script.job_thread import JobThread


class JobProgressHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, url_str=''):
        if url_str == '':
            return
        if url_str == 'start':
            self.start()
        if url_str == 'get':
            self.info()
        if url_str == 'list':
            self.list()
        if url_str == 'remove':
            self.remove()

    @tornado.web.authenticated
    @db.commit_on_success
    def start(self):
        # JobProgress.create_table()
        #ShellLog.create_table()
        #查询job下所有的脚本
        try:
            job_id = self.args.get("job_id")
            for id in job_id:
                print id;
                list = Script.select().where(Script.job_id == id)
                max_num = len(list);
                pro = JobProgress()
                pro.uuid = get_uuid()
                pro.job_id = id
                pro.max_num = max_num
                pro.success_num = 0;
                pro.fail_num = 0;
                pro.status = 0;
                pro.result = -1;
                pro.save(force_insert=True)

                #开启线程执行脚本 并保存执行记录
                #for i in list:
                JobThread(pro.uuid);
            self.write({'success': True, 'content': '开始执行'})
        except Exception, e:
            self.write({'success': False, 'content': '服务器异常'})
            print Exception, e;



    @tornado.web.authenticated
    def info(self):
        try:
            pro_id = self.args.get("pro_id")
            list = ShellLog.select().where(ShellLog.process_id == pro_id)
            resp = []
            for data in list:
                resp.append(data.to_dict())

            self.write({'success': True, 'content': '查询成功', 'list': resp})
        except Exception, e:
            self.write({'success': False, 'content': '查询失败'})
            print Exception, e;

    @tornado.web.authenticated
    @db.commit_on_success
    def list(self):
        try:
            # 进程状态
            status = self.args.get("status")
            list = JobProgress.select().where(JobProgress.status == status)
            print len(list)
            resp = []
            for data in list:
                resp.append(data.to_dict())

            self.write({'success': True, 'content': '查询成功', 'list': resp})
        except Exception, e:
            self.write({'success': False, 'content': '查询失败'})
            print Exception, e

    @tornado.web.authenticated
    def remove(self):
        pass


#!/usr/bin/python
# coding=utf-8
#
# File Name: rask.py
# File Author: lidey
# File Created Date: 2015-11-27 16:22
import commands
import json
import time
import datetime
import tornado
from app.core.base_handler import BaseHandler
from app.model.job_model import Job
from app.model.user_model import User
from app.scheduler.shell_scheduler import ShellScheduler
from app.script.spark_script import SparkScript


class JobHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    @tornado.web.authenticated
    def get(self, url_str=''):
        if url_str == '':
            return
        if url_str == 'start':
            self.start()
        if url_str == 'remove':
            self.remove()
        if url_str == 'list':
            self.list()
        if url_str == 'add':
            self.add()

    @tornado.web.authenticated
    def post(self, url_str=''):
        if url_str == '':
            return
        if url_str == 'start':
            self.start()
        if url_str == 'remove':
            self.remove()
        if url_str == 'getUUID':
            self.getUUID()
        if url_str == 'deleteUUID':
            self.deleteUUID()
        if url_str == 'add':
            self.add()

    @tornado.web.authenticated
    def start(self):
        id = self.get_argument('id')
        name = self.get_argument('name')
        Job.create_table()

        out = SparkScript(hostname='10.211.55.15', username='root', password='admins').command()
        out = out.replace('\n', '<br/>')
        out = out.replace(' ', '&nbsp;')
        entity = User().find_uuid('asdas').to_json()
        ShellScheduler().add_job(name=name, uuid=id)

        self.write({'log': True, 'user':entity})


    @tornado.web.authenticated
    def remove(self):
        uuid = self.get_argument('id')
        ShellScheduler().remove_job(uuid)
        self.write({'log': True})

    @tornado.web.authenticated
    def list(self):
        list =  Job.select()
        resp = []
        for data in list:
            #data.createTime = time.mktime(data.createTime.timetuple())

            resp.append(data.to_dict())
            print resp
        self.write({'list': resp})

    @tornado.web.authenticated
    def getUUID(self):
        uuid =  self.args.get("id")
        print uuid
        job =  Job().find_uuid(uuid)

        self.write({'job': job.to_dict()})

    def deleteUUID(self):
        uuid = self.args.get("id")
        print uuid
        job =  Job().find_uuid(uuid)
        job.delete_uuid()

        self.write({'success':True,'job': job.to_dict()})
    def add(self):
        job = Job()
        job.title =  self.args.get("title")
        job.desc = self.args.get("content")
        job.uuid = self.args.get("id")
        job.createTime = datetime.datetime.now()
        job.save(force_insert=True)

        self.write({'log': True, 'job':job.to_dict()})
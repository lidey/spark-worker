#!/usr/bin/python
# coding=utf-8
#
# File Name: rask.py
# File Author: lidey 
# File Created Date: 2015-11-27 16:22
import commands
import tornado
from app.core.base_handler import BaseHandler
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

    @tornado.web.authenticated
    def start(self):
        # id = self.get_argument('id')
        # name = self.get_argument('name')
        out = SparkScript(hostname='10.211.55.15', username='root', password='admins').command()
        out = out.replace('\n', '<br/>')
        out = out.replace(' ', '&nbsp;')
        entity = User().find_uuid('asdas').to_json()
        # ShellScheduler().add_job(name=name, uuid=id)
        self.write({'log': out, 'user': entity})

    @tornado.web.authenticated
    def remove(self):
        uuid = self.get_argument('id')
        ShellScheduler().remove_job(uuid)
        self.write({'log': True})

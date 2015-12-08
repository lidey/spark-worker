#!/usr/bin/python
# coding=utf-8
#
# File Name: rask.py
# File Author: lidey
# File Created Date: 2015-11-27 16:22

import datetime
import tornado
from app.core.base_handler import BaseHandler
from app.model.job_model import Job
from app.scheduler.shell_scheduler import ShellScheduler


class JobHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    @tornado.web.authenticated
    def get(self, url_str=''):
        if url_str == '':
            return
        if url_str == 'remove':
            self.remove()
        if url_str == 'list':
            self.list()
        if url_str == 'add':
            self.add()
        if url_str == 'update':
            self.update()

    @tornado.web.authenticated
    def post(self, url_str=''):
        if url_str == '':
            return
        if url_str == 'remove':
            self.remove()
        if url_str == 'getUUID':
            self.getUUID()
        if url_str == 'deleteUUID':
            self.deleteUUID()
        if url_str == 'add':
            self.add()
        if url_str == 'update':
            self.update()


    @tornado.web.authenticated
    def remove(self):
        try:
            uuid = self.get_argument('id')
            ShellScheduler().remove_job(uuid)
            self.write({'success': True, 'message': '删除成功'})
        except Exception, e:
            self.write({'success': False, 'message': '删除失败'})
            print Exception, ':', e

    @tornado.web.authenticated
    def list(self):
        try:
            list = Job.select()
            resp = []
            for data in list:
                resp.append(data.to_dict())
                print resp
            self.write({'success': True, 'message': '查询成功', 'list': resp})
        except Exception, e:
            self.write({'success': False, 'message': '查询失败'})
            print Exception, ':', e

    @tornado.web.authenticated
    def getUUID(self):
        try:
            uuid = self.args.get("id")
            job = Job().find_uuid(uuid)

            self.write({'success': True, 'message': '查询成功', 'job': job.to_dict()})
        except Exception, e:
            self.write({'success': False, 'message': '查询失败'})
            print Exception, ':', e

    @tornado.web.authenticated
    def deleteUUID(self):
        try:
            uuid = self.args.get("id")
            job = Job().find_uuid(uuid)
            job.delete_uuid()
            self.write({'success': True, 'message': '删除成功', 'job': job.to_dict()})
        except Exception, e:
            self.write({'success': False, 'message': '删除失败'})
            print Exception, ':', e

    @tornado.web.authenticated
    def add(self):
        try:
            job = Job()
            job.title = self.args.get("title")
            job.desc = self.args.get("content")
            job.uuid = self.args.get("id")
            job.createTime = datetime.datetime.now()
            job.save(force_insert=True)
            self.write({'success': True, 'message': '添加成功', 'job':job.to_dict()})
        except Exception,e:
            self.write({'success': False, 'message': '添加失败'})
            print Exception, ':', e

    @tornado.web.authenticated
    def update(self):
        try:
            job = Job().find_uuid(self.args.get("id"))
            job.title = self.args.get("title")
            job.desc = self.args.get("content")
            print job.title
            job.save()

            self.write({'success': True,'message': '修改成功', 'job':job.to_dict()})
        except Exception, e:
            self.write({'success': False, 'message': '修改失败'})
            print Exception, ':', e
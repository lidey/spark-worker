#!/usr/bin/python
# coding=utf-8

import tornado
import uuid
from datetime import datetime
from app.core.base_handler import BaseHandler
from app.model.scheduler_model import Scheduler


class SchedulerHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    @tornado.web.authenticated
    def get(self, url_str=''):
        if url_str == '':
            return
        if url_str == 'list':
            self.list()
        if url_str == 'delete':
            self.delete()
        if url_str == 'save':
            self.save()
        if url_str == 'update':
            self.update()

    @tornado.web.authenticated
    def post(self, url_str=''):
        #scheduler = Scheduler()
        #scheduler.uuid = self.args.get('uuid')
        #scheduler.cron = self.args.get('cron')
        #scheduler.msg = self.args.get('msg')
        #self.scheduler = scheduler
        if url_str == '':
            return
        if url_str == 'list':
            self.list()
        if url_str == 'delete':
            self.delete()
        if url_str == 'save':
            self.save()
        if url_str == 'update':
            self.update()


    @tornado.web.authenticated
    def list(self):
        try:
            #Scheduler.create_table();
            schedulers = []
            for data in Scheduler.select():
                schedulers.append(data.to_dict())
                print schedulers
            self.write({"list": schedulers, 'success': True, 'message': '查询成功'})
        except Exception, e:
            print Exception, ':', e
            self.write({'success': False, 'message': '查询失败'})


    @tornado.web.authenticated
    def delete(self):
        try:
            print("删除进行了吗")
            scheduler = Scheduler.get(Scheduler.uuid == self.get_argument('uuid'))
            scheduler.delete_instance()
            self.write({'success': True, 'message': '删除成功', 'scheduler': scheduler.to_dict()})
        except Exception, e:
            self.write({'success': False, 'message': '删除失败'})
            print Exception, ':', e




    @tornado.web.authenticated
    def update(self):
        try:
            scheduler = Scheduler().find_uuid(self.args.get("id"))
            scheduler.cron = self.args.get("cron")
            scheduler.msg = self.args.get("msg")
            scheduler.save()
            self.write({'success': True, 'message': '更新成功', 'scheduler': scheduler.to_dict()})
        except Exception, e:
            self.write({'success': False, 'message': '更新失败'})
            print Exception, ':', e

    @tornado.web.authenticated
    def save(self):
        try:
            #scheduler = self.scheduler

            #print ("UUID:"+scheduler.uuid)
            #scheduler = Scheduler()
            if self.args.get("uuid") == None:
                scheduler = Scheduler()
                scheduler.uuid = str(uuid.uuid1())
                scheduler.cron = self.args.get("cron")
                scheduler.msg = self.args.get("msg")
                scheduler.name = self.args.get("name")
                scheduler.created_time = datetime.now()
                scheduler.save(force_insert=True)
                print("保存成功吗")
                self.write({'success': True, 'message': '保存成功', 'scheduler': scheduler.to_dict()})
            else:
                scheduler = Scheduler.get(Scheduler.uuid == self.args.get("uuid"))
                scheduler.cron = self.args.get("cron")
                scheduler.msg = self.args.get("msg")
                scheduler.save()
        except Exception, e:
            self.write({'success': False, 'message': '保存失败'})
            print Exception, ':', e
    @tornado.web.authenticated
    def getUUID(self):
        try:
            uuid = self.args.get("UUID")
            print uuid
            scheduler = Scheduler.find_uuid(uuid)
            self.write({'scheduler': scheduler.to_dict(), 'success': True, 'message': '保存成功'})
        except Exception, e:
            self.write({'success': False, 'message': '保存失败'})
            print Exception, ':', e

    @tornado.web.authenticated
    def start_job(self):
        try:
            pass
        except Exception, e:
            print Exception, ':', e
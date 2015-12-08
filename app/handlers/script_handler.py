#!/usr/bin/python
# coding=utf-8
import datetime
import tornado

from app.core.base_handler import BaseHandler

from app.model.script_model import Script


class ScriptHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self, url_str=''):
        if url_str == '':
            return
        if url_str == 'save':
            self.save()
        if url_str == 'update':
            self.update()
        if url_str == 'get':
            self.info()
        if url_str == 'list':
            self.list()
        if url_str == 'remove':
            self.remove()

    @tornado.web.authenticated
    def get(self, url_str=''):
        if url_str == '':
            return

    @tornado.web.authenticated
    def save(self):
        try:
            script = Script()
            script.title = self.args.get("title")
            script.script = self.args.get("script")
            script.uuid = self.args.get("id")
            script.server_id = self.args.get("server_id")
            script.job_id = self.args.get("job_id")
            script.createTime = datetime.datetime.now()
            script.save(force_insert=True)
            self.write({'success': False, 'message': '添加成功', 'script': script.to_dict()})
        except Exception, e:
            self.write({'success': False, 'message': '添加失败'})
            print Exception, ':', e

    @tornado.web.authenticated
    def info(self):
        try:
            uuid = self.args.get("id")
            script = Script().find_uuid(uuid)
            self.write({'success': True, 'message': '查询成功', 'script': script.to_dict()})
        except Exception, e:
            self.write({'success': False, 'message': '查询失败'})
            print Exception, ':', e

    @tornado.web.authenticated
    def list(self):
        try:
            #Script.create_table()
            job_id = self.args.get("job_id")
            list = Script.select().where(Script.job_id == job_id)
            resp = []
            for data in list:
                resp.append(data.to_dict())
            self.write({'success': True, 'message': '查询成功', 'list': resp})
        except Exception, e:
            self.write({'success': False, 'message': '查询失败'})
            print Exception, ':', e

    @tornado.web.authenticated
    def remove(self):
        try:
            uuid = self.args.get("id")
            script = Script().find_uuid(uuid)
            script.delete_uuid()
            self.write({'success': True, 'message': '删除成功', 'script': script.to_dict()})
        except Exception, e:
            self.write({'success': False, 'message': '删除失败'})
            print Exception, ':', e

    @tornado.web.authenticated
    def update(self):
        try:
            script = Script().find_uuid(self.args.get("id"))
            script.title = self.args.get("title")
            script.script = self.args.get("script")
            script.server_id = self.args.get("server_id")
            script.save()

            self.write({'success': True, 'message': '修改成功', 'script': script.to_dict()})
        except Exception, e:
            self.write({'success': False, 'message': '修改失败'})
            print Exception, ':', e

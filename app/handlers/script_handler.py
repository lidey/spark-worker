#!/usr/bin/python
# coding=utf-8
import datetime
import tornado

from app.core.base_handler import BaseHandler

from app.model.script_model import Script
from app.model.server_model import Server
from app.script.server_script import ServerScript


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
        if url_str == 'test':
            self.test()

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
            script.desc = self.args.get("desc")
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
            # Script.create_table()
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
            script.desc = self.args.get("desc")
            script.save()

            self.write({'success': True, 'message': '修改成功', 'script': script.to_dict()})
        except Exception, e:
            self.write({'success': False, 'message': '修改失败'})
            print Exception, ':', e

    @tornado.web.authenticated
    def test(self):
        try:
            s = Server().get(Server.uuid == self.args.get("server_id"))
            test = ServerScript(server=s)
            out, err = test.command(self.args.get("script"))
            self.write({'success': True, 'result': out, 'error': err})
        except Exception, e:
            self.write({'success': False, 'content': '测试失败'})
            print Exception, ':', e

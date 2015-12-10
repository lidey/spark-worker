#!/usr/bin/python
# coding=utf-8
#
# File Name: rask.py
# File Author: lidey 
# File Created Date: 2015-11-27 16:22
import commands
import uuid
from datetime import datetime
import select

import thread
import tornado
from paramiko import AuthenticationException
from paramiko.ssh_exception import NoValidConnectionsError
from app.core.base_handler import BaseHandler
from app.model.server_model import Server
from app.script.server_script import ServerScript


class ServerHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    @tornado.web.authenticated
    def post(self, url_str=''):
        if url_str == '':
            return

        server = Server()
        server.uuid = self.args.get('uuid')
        server.title = self.args.get('title')
        server.description = self.args.get('description')
        server.host = self.args.get('host')
        server.version = self.args.get('version').get('key')
        server.name = self.args.get('name')
        server.password = self.args.get('password')
        server.cpu = self.args.get('cpu')
        server.core = self.args.get('core')
        server.processor = self.args.get('processor')
        server.men = self.args.get('men')
        self.server = server

        if url_str == 'save':
            self.save()
        if url_str == 'test':
            self.test()

    @tornado.web.authenticated
    def get(self, url_str=''):
        if url_str == '':
            return
        if url_str == 'info':
            self.info()
        if url_str == 'list':
            self.list()
        if url_str == 'remove':
            self.remove()

    @tornado.web.authenticated
    def save(self):
        server = self.server
        if server.uuid == None:
            server.uuid = str(uuid.uuid1())
            server.created_time = datetime.now()
            server.save(force_insert=True)
        else:
            server.save()
            server.created_time = datetime.now()
        self.write({'success': True, 'content': '服务器保存成功.', 'server': server.to_dict()})

    @tornado.web.authenticated
    def info(self):
        server = Server.get(Server.uuid == self.get_argument('uuid'))
        self.write(server.to_dict())

    @tornado.web.authenticated
    def list(self):
        servers = []
        for server in Server.select():
            servers.append(server.to_dict())
        self.write({'servers': servers})

    @tornado.web.authenticated
    def remove(self):
        server = Server.get(Server.uuid == self.get_argument('uuid'))
        server.delete_instance()
        self.write({'success': True, 'content': '服务器删除成功.'})

    @tornado.web.authenticated
    def test(self):
        try:
            script = ServerScript(server=self.server)
            cpu_num, _ = script.command("cat /proc/cpuinfo |grep 'physical id'|sort |uniq|wc -l")
            core_num, _ = script.command("cat /proc/cpuinfo |grep 'cores'|uniq|awk '{print $4}'")
            processor_num, _ = script.command("cat /proc/cpuinfo |grep 'processor'|sort |uniq|wc -l")
            men, _ = script.command("free -m | grep Mem | awk '{print $2}'")
            script.close()
            self.write(
                {'success': True, 'content': '服务器链接测试通过.', 'cpu': cpu_num, 'core': core_num, 'processor': processor_num,
                 'men': men})
        except NoValidConnectionsError:
            self.write({'success': False, 'content': '服务器链接错误.'})
        except AuthenticationException:
            self.write({'success': False, 'content': '账号或密码错误.'})
        except IndentationError:
            self.write({'success': False, 'content': '服务器链接错误.'})

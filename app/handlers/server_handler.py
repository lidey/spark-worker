#!/usr/bin/python
# coding=utf-8
#
# File Name: rask.py
# File Author: lidey 
# File Created Date: 2015-11-27 16:22
import commands
import json
import threading
import uuid
import time
from datetime import datetime

import select

import sys
import tornado
from paramiko import AuthenticationException
from paramiko.ssh_exception import NoValidConnectionsError
from tornado.websocket import WebSocketClosedError

from app.core.base_handler import BaseHandler
from app.model.server_model import Server
from app.script.server_script import ServerScript, Tty


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
            men, _ = script.command("free -m | grep Mem | awk '{print $2}'")
            script.close()
            self.write({'success': True, 'content': '服务器链接测试通过.', 'cpu': cpu_num, 'core': core_num, 'men': men})
        except NoValidConnectionsError:
            self.write({'success': False, 'content': '服务器链接错误.'})
        except AuthenticationException:
            self.write({'success': False, 'content': '账号或密码错误.'})
        except IndentationError:
            self.write({'success': False, 'content': '服务器链接错误.'})


class MyThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(MyThread, self).__init__(*args, **kwargs)

    def run(self):
        try:
            super(MyThread, self).run()
        except WebSocketClosedError:
            pass


class WebTty(Tty):
    def __init__(self, *args, **kwargs):
        super(WebTty, self).__init__(*args, **kwargs)
        self.ws = None
        self.data = ''
        self.input_mode = False


class WebTerminalHandler(tornado.websocket.WebSocketHandler):
    def data_received(self, chunk):
        pass

    clients = []
    tasks = []

    def __init__(self, *args, **kwargs):
        self.term = None
        self.id = 0
        self.user = None
        self.ssh = None
        self.channel = None
        super(WebTerminalHandler, self).__init__(*args, **kwargs)

    def check_origin(self, origin):
        return True

    def open(self):
        server = Server.get(Server.uuid == self.get_argument('uuid'))
        self.term = WebTty(server)
        self.ssh = self.term.get_connection()
        self.channel = self.ssh.invoke_shell(term='xterm')
        WebTerminalHandler.tasks.append(MyThread(target=self.forward_outbound))
        WebTerminalHandler.clients.append(self)

        for t in WebTerminalHandler.tasks:
            if t.is_alive():
                continue
            try:
                t.setDaemon(True)
                t.start()
            except RuntimeError:
                pass

    def on_message(self, message):
        data = json.loads(message)
        if not data:
            return
        if data.get('data'):
            self.term.input_mode = True
            if str(data['data']) in ['\r', '\n', '\r\n']:
                if self.term.vim_flag:
                    match = self.term.ps1_pattern.search(self.term.vim_data)
                    if match:
                        self.term.vim_flag = False
                        vim_data = self.term.deal_command(self.term.vim_data)[0:200]

                self.term.vim_data = ''
                self.term.data = ''
                self.term.input_mode = False
            if not self.channel.closed:
                self.channel.send(data['data'])

    def on_close(self):
        if self in WebTerminalHandler.clients:
            WebTerminalHandler.clients.remove(self)
        try:
            self.ssh.close()
            self.close()
        except AttributeError:
            pass

    def forward_outbound(self):
        try:
            data = ''
            while True:
                r, w, e = select.select([self.channel, sys.stdin], [], [])
                if self.channel in r:
                    recv = self.channel.recv(1024)
                    if not len(recv):
                        return
                    data += recv
                    if self.term.vim_flag:
                        self.term.vim_data += recv
                    try:
                        self.write_message(json.dumps({'data': data}))
                        if self.term.input_mode and not self.term.is_output(data):
                            self.term.data += data
                        data = ''
                    except UnicodeDecodeError:
                        pass
        except IndexError:
            pass

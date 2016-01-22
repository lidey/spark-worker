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
from app.core.base_thread import WebSocketThread
from app.model.server_model import Server
from app.model.spark_model import Spark
from app.script.server_script import ServerScript, Tty, WebTty


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
        server.type = self.args.get('type')
        server.version = self.args.get('version').get('key')
        server.name = self.args.get('name')
        server.password = self.args.get('password')
        server.processor = self.args.get('processor')
        server.memory = self.args.get('memory')
        server.path = self.args.get('path')
        if server.type == 'Spark':
            spark = Spark()
            spark.uuid = self.args.get('spark').get('uuid')
            spark.path = self.args.get('spark').get('path')
            spark.web_ui = self.args.get('spark').get('web_ui')
            spark.url = self.args.get('spark').get('url')
            spark.rest_url = self.args.get('spark').get('rest_url')
            spark.max_memory = self.args.get('spark').get('max_memory')
            spark.max_processor = self.args.get('spark').get('max_processor')
            spark.variables = json.dumps(self.args.get('spark').get('variables'))
            server.spark = spark
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

    def save(self):
        """
        保存服务器链接信息
        :return: 处理结果
        """
        server = self.server
        if server.uuid == None:
            server.uuid = str(uuid.uuid1())
            server.created_time = datetime.now()
            server.save(force_insert=True)
            if server.type == 'Spark':
                spark = server.spark
                spark.server = server
                spark.uuid = str(uuid.uuid1())
                spark.save(force_insert=True)

        else:
            server.save()
            if server.type == 'Spark':
                spark = server.spark
                spark.save()
        self.write({'success': True, 'content': '服务器保存成功.', 'uuid': server.uuid})

    def info(self):
        """
        获取服务器链接信息
        :return: 链接信息
        """
        server = Server.get(Server.uuid == self.get_argument('uuid'))
        server_dict = server.to_dict()
        if server.type == 'Spark':
            spark = Spark.select().join(Server).where(Server.uuid == server.uuid).get()
            server_dict['spark'] = spark.to_dict()
        self.write(server_dict)

    def list(self):
        """
        获取服务器链接列表
        :return: 链接列表
        """
        servers = []
        for server in Server.select():
            servers.append(server.to_dict())
        self.write({'servers': servers})

    def remove(self):
        """
        删除服务器链接信息
        :return: 处理结果
        """
        server = Server.get(Server.uuid == self.get_argument('uuid'))
        server.delete_instance()
        self.write({'success': True, 'content': '服务器删除成功.'})

    def test(self):
        """
        测试服务器链接信息
        :return: 处理结果
        """
        try:
            script = ServerScript(server=self.server)
            processor, _ = script.command("cat /proc/cpuinfo |grep 'processor'|sort |uniq|wc -l")
            memory, _ = script.command("free -m | grep Mem | awk '{print $2}'")
            script.close()
            self.write({'success': True, 'content': '服务器链接测试通过.', 'processor': processor, 'memory': memory})
        except NoValidConnectionsError:
            self.write({'success': False, 'content': '服务器链接错误.'})
        except AuthenticationException:
            self.write({'success': False, 'content': '账号或密码错误.'})
        except IndentationError:
            self.write({'success': False, 'content': '服务器链接错误.'})


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
        WebTerminalHandler.tasks.append(WebSocketThread(target=self.forward_outbound))
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
                print data['data']
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


class WebTerminalKillHandler(BaseHandler):
    def get(self):
        ws_id = self.get_argument('id')
        for ws in WebTerminalHandler.clients:
            print ws.id
            if ws.id == int(ws_id):
                ws.close()

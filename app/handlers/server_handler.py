#!/usr/bin/python
# coding=utf-8
#
# File Name: rask.py
# File Author: lidey 
# File Created Date: 2015-11-27 16:22
import json
import uuid
import select
import sys
import tornado.web
import tornado.websocket

from paramiko import AuthenticationException
from paramiko.ssh_exception import NoValidConnectionsError

from app.core.base_handler import BaseHandler
from app.core.base_thread import WebSocketThread
from app.model.server_model import Server, Folder
from app.model.spark_model import Spark
from app.script.server_script import ServerScript, WebTty


class ServerHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    @tornado.web.authenticated
    def post(self, url_first='', url_second=''):
        if url_first == '':
            return
        if url_first == 'folder' and url_second == 'save':
            folder = Folder()
            folder.uuid = self.args.get('uuid')
            folder.title = self.args.get('title')
            folder.description = self.args.get('description')
            return self.folder_save(folder)

        if url_first == 'save':
            server = Server()
            server.uuid = self.args.get('uuid')
            server.f_uuid = self.args.get('f_uuid')
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
            return self.server_save(server)

    @tornado.web.authenticated
    def get(self, url_first='', url_second=''):
        if url_first == '':
            return
        if url_first == 'folder' and url_second == 'tree':
            return self.folder_tree()
        if url_first == 'folder' and url_second == 'info':
            return self.folder_info()
        if url_first == 'folder' and url_second == 'remove':
            return self.folder_remove()
        if url_first == 'info':
            return self.server_info()
        if url_first == 'list':
            return self.server_list()
        if url_first == 'all':
            return self.server_all()
        if url_first == 'remove':
            return self.server_remove()
        if url_first == 'test':
            return self.server_test()

    def folder_tree(self):
        """
        查询数据库链接及包含的目录结构
        :return: 树形数据集
        """
        tree = []
        for folder in Folder.select():
            tree.append(folder.to_tree())
        self.write({'tree': tree})

    def folder_save(self, folder):
        """
        保存服务器链接目录分类信息
        :param folder: 目录分类信息
        :return: 处理结果
        """
        if folder.uuid is None:
            folder.uuid = str(uuid.uuid1())
            folder.save(force_insert=True)
        else:
            folder.save()
        self.write({'success': True, 'content': '目录分类保存成功.'})

    def folder_info(self):
        """
        获取服务器链接目录分类信息
        :return: 目录分类信息
        """
        self.write(Folder.get(Folder.uuid == self.get_argument('uuid')).to_dict())

    def folder_remove(self):
        """
        删除服务器链接目录分类
        :return: 处理结果
        """
        Folder.get(Folder.uuid == self.get_argument('uuid')).delete_instance()
        self.write({'success': True, 'content': '目录分类删除成功.'})

    def server_save(self, server):
        """
        保存服务器链接信息
        :param server: 服务器链接信息
        :return: 处理结果
        """
        if server.uuid is None:
            server.uuid = str(uuid.uuid1())
            server.folder = Folder.get(Folder.uuid == server.f_uuid)
            server.save(force_insert=True)

        else:
            server.save()
        self.write({'success': True, 'content': '服务器保存成功.'})

    def server_info(self):
        """
        获取服务器链接信息
        :return: 链接信息
        """
        self.write(Server.get(Server.uuid == self.get_argument('uuid')).to_dict())

    def server_list(self):
        """
        获取服务器链接列表
        :return: 链接列表
        """
        servers = []
        for server in Server.select().join(Folder).where(Folder.uuid == self.get_argument('f_uuid')):
            servers.append(server.to_dict())
        self.write({'servers': servers})

    def server_all(self):
        """
        获取服务器链接列表
        :return: 链接列表
        """
        servers = []
        for server in Server.select().join(Folder):
            servers.append(server.to_dict())
        self.write({'servers': servers})

    def server_remove(self):
        """
        删除服务器链接信息
        :return: 处理结果
        """
        server = Server.get(Server.uuid == self.get_argument('uuid'))
        server.delete_instance()
        self.write({'success': True, 'content': '服务器删除成功.'})

    def server_test(self):
        """
        测试服务器链接信息
        :return: 处理结果
        """
        try:
            script = ServerScript(Server.get(Server.uuid == self.get_argument('uuid')))
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
        """
        建立web socket连接
        :return:
        """
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
        """
        发送信息
        :param message:信息
        :return:
        """
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

                self.term.vim_data = ''
                self.term.data = ''
                self.term.input_mode = False
            if not self.channel.closed:
                print data['data']
                self.channel.send(data['data'])

    def on_close(self):
        """
        关闭连接
        :return:
        """
        if self in WebTerminalHandler.clients:
            WebTerminalHandler.clients.remove(self)
        try:
            self.ssh.close()
            self.close()
        except AttributeError:
            pass

    def forward_outbound(self):
        """
        监听ssh连接发送回调信息
        :return:
        """
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

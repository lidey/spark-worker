#!/usr/bin/python
# coding=utf-8
#
# File Name: rask.py
# File Author: lidey 
# File Created Date: 2015-11-27 16:22
import json
import os
import uuid
import zipfile

import select

import sys

import tornado
import tornado.websocket
from jinja2 import Environment, PackageLoader

from app.core.base_handler import BaseHandler
from app.core.base_thread import WebSocketThread
from app.model.spark_model import Spark, SparkJob, SparkJobLog
from app.script.server_script import WebTty, ServerScript
from app.script.spark_thread import SparkJobThread, CreateSparkJobThread
from config import system, sparkConfig


class SparkHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    @tornado.web.authenticated
    def post(self, url_first='', url_second=''):
        if url_first == '':
            return
        if url_first == 'job':
            job = SparkJob()
            job.uuid = self.args.get('uuid')
            job.s_uuid = self.args.get('s_uuid')
            job.title = self.args.get('title')
            job.description = self.args.get('description')
            job.main_class = self.args.get('main_class')
            job.main_jar = self.args.get('main_jar')
            job.master = self.args.get('master')
            job.arguments = self.args.get('arguments')
            job.processor = self.args.get('processor')
            job.memory = self.args.get('memory')
            self.job = job
        if url_first == 'job' and url_second == 'save':
            self.job_save()
        if url_first == 'job' and url_second == 'upload_jar':
            self.job_upload_jar()

    @tornado.web.authenticated
    def get(self, url_first='', url_second=''):
        if url_first == '':
            return
        if url_first == 'list':
            self.list()
        if url_first == 'info':
            self.info()
        if url_first == 'job' and url_second == 'list':
            self.job_list()
        if url_first == 'job' and url_second == 'info':
            self.job_info()
        if url_first == 'job' and url_second == 'remove_jar':
            self.job_remove_jar()
        if url_first == 'job' and url_second == 'open_jars':
            self.job_open_jars()
        if url_first == 'job' and url_second == 'remove':
            self.job_remove()
        if url_first == 'job' and url_second == 'start':
            self.job_start()
        if url_first == 'job' and url_second == 'log_list':
            self.job_log_list()
        if url_first == 'job' and url_second == 'log':
            self.job_log()

    def info(self):
        """
        获取Spark服务器信息
        :return: 服务器信息
        """
        spark = Spark.get(Spark.uuid == self.get_argument('uuid'))
        self.write(spark.to_dict())

    def list(self):
        """
        获取Spark服务器列表
        :return: 服务器列表
        """
        sparks = []
        for spark in Spark.select():
            sparks.append(spark.to_dict())
        self.write({'sparks': sparks})

    def job_list(self):
        """
        获取Spark作业列表
        :return: 链接列表
        """
        jobs = []
        for job in SparkJob.select().join(Spark).where(Spark.uuid == self.get_argument('s_uuid')):
            jobs.append(job.to_dict())
        self.write({'jobs': jobs})

    def job_upload_jar(self):
        """
        上传jar包
        :return:
        """
        upload_path = os.path.join(system['upload_file'],
                                   sparkConfig['upload_path'] + '/' + self.request.headers['uuid'])  # 文件的暂存路径

        if os.path.exists(upload_path):
            print('文件目录存在')
        else:
            os.makedirs(upload_path)
        file_metas = self.request.files['file']  # 提取表单中‘name’为‘file’的文件元数据
        for meta in file_metas:
            file_name = meta['filename']
            file_path = os.path.join(upload_path, file_name)
            with open(file_path, 'wb') as up:  # 有些文件需要已二进制的形式存储，实际中可以更改
                up.write(meta['body'])
        self.write({'success': True, 'content': 'jar包上传成功.', 'file_name': file_name})

    def job_remove_jar(self):
        """
        删除jar 包
        :return:
        """
        upload_path = os.path.join(system['upload_file'],
                                   sparkConfig['upload_path'] + '/' + self.get_argument('uuid'))  # 文件的暂存路径
        upload_file = os.path.join(upload_path, self.get_argument('file_name'))  # 文件的暂存路径
        if os.path.isfile(upload_file):
            os.remove(upload_file)
        self.write({'success': True, 'content': 'jar包删除成功.'})

    def job_open_jars(self):
        """
        获取作业jar包中的类列表
        :return:类列表
        """
        upload_path = os.path.join(system['upload_file'],
                                   sparkConfig['upload_path'] + '/' + self.get_argument('uuid'))  # 文件的暂存路径
        classes = []
        for jar in os.listdir(upload_path):
            jar_file = os.path.join(upload_path, jar)
            if os.path.isfile(jar_file) and zipfile.is_zipfile(jar_file):
                zfobj = zipfile.ZipFile(jar_file)
                for name in zfobj.namelist():
                    name = name.replace('/', '.')
                    if name.startswith(sparkConfig['startswith']) and name.find('$') == -1 and name.endswith('.class'):
                        name = name.replace('.class', '')
                        classes.append({'name': name, 'jar': jar})
        self.write({'classes': classes})

    def job_save(self):
        """
        保存Spark作业信息
        :return: 处理结果
        """
        job = self.job
        if job.uuid is None:
            job.uuid = str(uuid.uuid1())
            job.spark = Spark.get(Spark.uuid == job.s_uuid)
            job.save(force_insert=True)
        else:
            job.save()
        self.write({'success': True, 'content': '作业保存成功.'})

    def job_info(self):
        """
        获取Spark服务器信息
        :return: 服务器信息
        """
        job = SparkJob.get(SparkJob.uuid == self.get_argument('uuid'))
        job_dict = job.to_dict()
        job_dict['jars'] = []
        upload_path = os.path.join(system['upload_file'], sparkConfig['upload_path'] + '/' + job.uuid)
        for jar in os.listdir(upload_path):
            if os.path.isfile(os.path.join(upload_path, jar)):
                job_dict['jars'].append(jar)
        self.write(job_dict)

    def job_remove(self):
        """
        删除Spark作业信息
        :return: 处理结果
        """
        job = SparkJob.get(SparkJob.uuid == self.get_argument('uuid'))
        job.delete_instance()
        self.write({'success': True, 'content': '作业删除成功.'})

    def job_start(self):
        """
        删除Spark作业信息
        :return: 处理结果
        """
        # SparkJobThread(self.get_argument('uuid'))
        CreateSparkJobThread(self.get_argument('uuid'))
        self.write({'success': True, 'content': '作业启动成功.'})

    def job_log_list(self):
        """
        获取Spark 作业日志列表
        :return: 作业日志列表
        """
        logs = []
        for log in SparkJobLog.select(SparkJobLog, SparkJob).join(SparkJob).order_by(SparkJobLog.created_time.desc()):
            logs.append(log.to_dict())
        self.write({'logs': logs})

    def job_log(self):
        """
        获取Spark 作业日志信息
        :return: 日志信息
        """
        log = SparkJobLog.get(SparkJobLog.uuid == self.get_argument('uuid'))
        log_dict = log.to_dict()
        log_dict['std_out'] = log.std_out
        log_dict['std_err'] = log.std_err
        self.write(log_dict)


class SparkTerminalHandler(tornado.websocket.WebSocketHandler):
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
        super(SparkTerminalHandler, self).__init__(*args, **kwargs)

    def check_origin(self, origin):
        return True

    def open(self):

        spark_job = SparkJob.get(SparkJob.uuid == self.get_argument('uuid'))
        spark = spark_job.spark

        self.term = WebTty(spark.server)
        self.ssh = self.term.get_connection()
        self.channel = self.ssh.invoke_shell()
        SparkTerminalHandler.tasks.append(WebSocketThread(target=self.forward_outbound))
        SparkTerminalHandler.clients.append(self)
        for t in SparkTerminalHandler.tasks:
            if t.is_alive():
                continue
            try:
                t.setDaemon(True)
                t.start()
            except RuntimeError:
                pass

        job_log = SparkJobLog()
        job_log.uuid = str(uuid.uuid1())
        job_log.job = spark_job

        self.write_message(json.dumps({'data': '开始上传 Jar 文件:'}))
        job_log.std_out = '开始上传 Jar 文件:'
        upload_path = os.path.join(system['upload_file'], sparkConfig['upload_path'] + '/' + spark_job.uuid)
        remotepath = os.path.join(spark.server.path, sparkConfig['upload_path'] + '/' + job_log.uuid)
        server_script = ServerScript(spark.server)
        spark_job.jars = []
        for file in os.listdir(upload_path):
            if os.path.isfile(os.path.join(upload_path, file)):
                server_script.upload(os.path.join(upload_path, file), os.path.join(remotepath, file))
                spark_job.jars.append(os.path.join(remotepath, file))
                self.write_message(json.dumps({'data': '文件{0}上传成功.'.format(file)}))
                job_log.std_out += '文件{0}上传成功.'.format(file)
        server_script.close()
        self.write_message(json.dumps({'data': 'Jar 文件上传完成,开始提交Spark 作业.'}))
        job_log.std_out += 'Jar 文件上传完成,开始提交Spark 作业.'

        env = Environment(loader=PackageLoader('app.handlers', 'templates'))
        template = env.get_template('spark_submit.jinja2')
        shell = template.render(spark=spark, job=spark_job, system=system)

        self.channel.send('\r')
        self.channel.send(shell)
        self.channel.send('\r')
        job_log.shell = shell
        job_log.status = 'RUNNING'
        job_log.save(force_insert=True)
        self.job_log = job_log
        self.term.output_mode = True

    def on_message(self, message):
        pass

    def on_close(self):
        if self in SparkTerminalHandler.clients:
            SparkTerminalHandler.clients.remove(self)
        try:
            self.ssh.close()
            self.close()
        except AttributeError:
            pass

    def forward_outbound(self):
        try:
            self.term.output_mode = False
            while True:
                r, w, e = select.select([self.channel, sys.stdin], [], [])
                if self.channel in r:
                    recv = self.channel.recv(1024)
                    if not len(recv):
                        return
                    try:
                        if self.term.output_mode:
                            self.job_log.std_out += recv
                            self.job_log.save()
                            self.write_message(json.dumps({'data': recv}))
                    except UnicodeDecodeError:
                        pass
        except IndexError:
            pass

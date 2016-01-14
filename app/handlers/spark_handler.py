#!/usr/bin/python
# coding=utf-8
#
# File Name: rask.py
# File Author: lidey 
# File Created Date: 2015-11-27 16:22
import commands
import json
import os
import uuid
import zipfile
from datetime import datetime

import tornado

from app.core.base_handler import BaseHandler
from app.model.spark_model import Spark, SparkJob
from config import system


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
        upload_path = os.path.join(system['upload_file'], 'spark_jobs/' + self.request.headers['uuid'])  # 文件的暂存路径

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
        upload_path = os.path.join(system['upload_file'], 'spark_jobs/' + self.get_argument('uuid'))  # 文件的暂存路径
        upload_file = os.path.join(upload_path, self.get_argument('file_name'))  # 文件的暂存路径
        if os.path.isfile(upload_file):
            os.remove(upload_file)
        self.write({'success': True, 'content': 'jar包删除成功.'})

    def job_open_jars(self):
        """
        删除jar 包
        :return:
        """
        upload_path = os.path.join(system['upload_file'], 'spark_jobs/' + self.get_argument('uuid'))  # 文件的暂存路径
        classes = []
        for jar in os.listdir(upload_path):
            jar_file = os.path.join(upload_path, jar)
            if os.path.isfile(jar_file) and zipfile.is_zipfile(jar_file):
                zfobj = zipfile.ZipFile(jar_file)
                for name in zfobj.namelist():
                    # if name.endswith('/'):
                    if name.find('$') == -1 and name.endswith('.class'):
                        name = name.replace('.class', '').replace('/', '.')
                        classes.append({'name': name, 'jar': jar})
                        print name
                        # os.remove(upload_file)
        self.write({'classes': classes})

    def job_save(self):
        """
        保存Spark作业信息
        :return: 处理结果
        """
        job = self.job
        if job.uuid == None:
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
        upload_path = os.path.join(system['upload_file'], 'spark_jobs/' + job.uuid)
        for file in os.listdir(upload_path):
            if os.path.isfile(os.path.join(upload_path, file)):
                job_dict['jars'].append(file)
        self.write(job_dict)

    def job_remove(self):
        """
        删除Spark作业信息
        :return: 处理结果
        """
        job = SparkJob.get(SparkJob.uuid == self.get_argument('uuid'))
        job.delete_instance()
        self.write({'success': True, 'content': '作业删除成功.'})

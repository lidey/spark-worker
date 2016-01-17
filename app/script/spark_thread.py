#!/usr/bin/python
# coding=utf-8
import os
import threading
import uuid

import select

import sys
from jinja2 import Environment, PackageLoader

from app.model.spark_model import SparkJob, SparkJobLog
from app.script.server_script import ServerScript
from config import system, sparkConfig


class SparkJobThread(threading.Thread):
    def __init__(self, uuid):
        threading.Thread.__init__(self)
        spark_job = SparkJob.get(SparkJob.uuid == uuid)
        spark = spark_job.spark
        self.spark_job = spark_job
        self.spark = spark
        self.start()

    def run(self):

        job_log = SparkJobLog()
        job_log.uuid = str(uuid.uuid1())
        job_log.job = self.spark_job

        job_log.status = 'INIT'
        job_log.save(force_insert=True)

        content = '开始上传 Jar 文件:\n'
        upload_path = os.path.join(system['upload_file'], sparkConfig['upload_path'] + '/' + self.spark_job.uuid)
        remote_path = os.path.join(self.spark.server.path, sparkConfig['upload_path'] + '/' + job_log.uuid)
        server_script = ServerScript(self.spark.server)
        try:
            self.spark_job.jars = []
            for f in os.listdir(upload_path):
                if os.path.isfile(os.path.join(upload_path, f)):
                    server_script.upload(os.path.join(upload_path, f), os.path.join(remote_path, f))
                    self.spark_job.jars.append(os.path.join(remote_path, f))
                    content += '文件{0}上传成功.\n'.format(f)
            content += 'Jar 文件上传完成,开始提交Spark 作业.\n'

            env = Environment(loader=PackageLoader('app.handlers', 'templates'))
            template = env.get_template('spark_submit.jinja2')
            shell = template.render(spark=self.spark, job=self.spark_job, system=system)

            job_log.shell = shell
            job_log.status = 'RUNNING'
            job_log.std_info = content
            job_log.save()

            _, std_out, std_info = server_script.exec_command(shell)
            job_log.std_out = std_out.read()
            job_log.status = 'FINISH'
            for line in std_info.readlines():
                job_log.std_info += str(line)
                if line.startswith('Exception in thread '):
                    job_log.status = 'ERROR'
        except Exception, e:
            print e
            job_log.std_info = 'Spark 作业执行错误:{0}.\n'.format(e.message)
            job_log.status = 'ERROR'
        finally:
            for f in self.spark_job.jars:
                server_script.remove_file(f)
            server_script.remove_dir(remote_path)
            job_log.std_info += 'Spark 作业完成,清理临时文件.\n'
            job_log.save()
            server_script.close()
        pass

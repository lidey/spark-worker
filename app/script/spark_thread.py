#!/usr/bin/python
# coding=utf-8
import json
import os
import threading
import uuid

import time
from jinja2 import Environment, PackageLoader
from tornado import httpclient

from app.core.base_model import db
from app.core.base_scheduler import scheduler
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
            job_log.std_err = content
            job_log.save()

            _, std_out, std_err = server_script.exec_command(shell)
            job_log.std_out = std_out.read()
            job_log.status = 'FINISH'
            for line in std_err.readlines():
                job_log.std_err += str(line)
                if line.startswith('Exception in thread '):
                    job_log.status = 'ERROR'
        except Exception, e:
            print e
            job_log.std_err = 'Spark 作业执行错误:{0}.\n'.format(e.message)
            job_log.status = 'ERROR'
        finally:
            for f in self.spark_job.jars:
                server_script.remove_file(f)
            server_script.remove_dir(remote_path)
            job_log.std_err += 'Spark 作业完成,清理临时文件.\n'
            job_log.save()
            server_script.close()
        pass


class CreateSparkJobThread(threading.Thread):
    """

    """

    def __init__(self, uuid):
        threading.Thread.__init__(self)
        spark_job = SparkJob.get(SparkJob.uuid == uuid)
        spark = spark_job.spark
        self.spark_job = spark_job
        self.spark = spark
        self.start()

    def run(self):
        """

        :return:
        """
        job_log = SparkJobLog()
        job_log.uuid = str(uuid.uuid1())
        job_log.job = self.spark_job

        server_script = ServerScript(self.spark.server)
        upload_path = os.path.join(system['upload_file'], sparkConfig['upload_path'] + '/' + self.spark_job.uuid)
        remote_path = os.path.join(self.spark.server.path, sparkConfig['upload_path'] + '/' + job_log.uuid)
        self.spark_job.jars = ''
        for f in os.listdir(upload_path):
            if os.path.isfile(os.path.join(upload_path, f)):
                server_script.upload(os.path.join(upload_path, f), os.path.join(remote_path, f))
                self.spark_job.jars += 'file:{0},'.format(os.path.join(remote_path, f))

        job_log.shell = json.dumps({
            "action": "CreateSubmissionRequest",
            "appArgs": self.spark_job.arguments.split(','),
            "appResource": 'file:{0}'.format(os.path.join(remote_path, self.spark_job.main_jar)),
            "clientSparkVersion": "1.6.0",
            "environmentVariables": {
                "SPARK_SCALA_VERSION": "2.10",
                "SPARK_CONF_DIR": "{0}/conf".format(self.spark.path),
                "SPARK_HOME": self.spark.path,
                "SPARK_ENV_LOADED": "1"
            },
            "mainClass": self.spark_job.main_class,
            "sparkProperties": {
                "spark.executor.memory": "{0}M".format(self.spark_job.memory),
                "spark.total.executor.cores": "{0}".format(self.spark_job.processor),
                "spark.jars": self.spark_job.jars,
                "spark.driver.supervise": "false",
                "spark.app.name": self.spark_job.title,
                "spark.eventLog.enabled": "true",
                "spark.submit.deployMode": "cluster",
                "spark.master": self.spark_job.master
            }
        })
        job_log.std_err = ''
        http_client = httpclient.HTTPClient()
        try:
            create_job_request = httpclient.HTTPRequest(
                    url='{0}/v1/submissions/create'.format(self.spark.rest_url),
                    method='POST',
                    headers={'Content-Type': 'application/json', 'charset': 'UTF-8'},
                    body=job_log.shell, use_gzip=True, connect_timeout=200,
                    request_timeout=600)
            response = http_client.fetch(create_job_request)
            print response.body
            job = json.loads(response.body)
            job_log.app_id = job['submissionId']
            job_log.status = 'INIT'
            job_log.save(force_insert=True)
            if job['success']:
                time.sleep(3)
                spark_job_status(job_log)
        except httpclient.HTTPError as e:
            # HTTPError is raised for non-200 responses; the response
            # can be found in e.response.
            print("Error: " + str(e))
        except Exception as e:
            # Other errors are possible, such as IOError.
            print("Error: " + str(e))
        finally:
            db.close()
            http_client.close()
            server_script.close()
        pass


def spark_job_status(log):
    """

    :param log:
    :return:
    """
    job = log.job
    spark = job.spark
    server_script = ServerScript(spark.server)
    http_client = httpclient.HTTPClient()
    select_job_request = httpclient.HTTPRequest(
            url='{0}/v1/submissions/status/{1}'.format(
                    spark.rest_url, log.app_id),
            method='GET',
            headers={'Content-Type': 'application/json', 'charset': 'UTF-8'}, use_gzip=True, connect_timeout=200,
            request_timeout=600)
    response = http_client.fetch(select_job_request)
    job_status = json.loads(response.body)
    print response.body
    if job_status['success']:
        log.status = job_status['driverState']
        job_path = os.path.join(os.path.join(spark.path, 'work'), log.app_id)
        log.std_err = server_script.open_file(os.path.join(job_path, 'stderr')).read()
        log.std_out = server_script.open_file(os.path.join(job_path, 'stdout')).read()
        log.save()
        db.close()

        if 'RUNNING' != log.status and 'INIT' != log.status:
            remote_path = os.path.join(spark.server.path, sparkConfig['upload_path'] + '/' + log.uuid)
            for f in server_script.list_dir(remote_path):
                server_script.remove_file(os.path.join(remote_path, f))
            server_script.remove_dir(remote_path)


class UpdateSparkJobThread(threading.Thread):
    """

    """

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def run(self):
        """

        :return:
        """
        for log in SparkJobLog.select().where(SparkJobLog.status == 'RUNNING'):
            spark_job_status(log)
        db.close()
        return


def update_spark_job_status():
    """

    :return:
    """
    UpdateSparkJobThread()


# scheduler.add_job(update_spark_job_status, 'interval', seconds=30)

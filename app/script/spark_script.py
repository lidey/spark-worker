#!/usr/bin/python
# coding=utf-8
#
# File Name: spark_script.py
# File Author: 姚丰利(lidey) 
# File Created Date: 2015-11-30 17:04
import paramiko


class SparkScript:
    def __init__(self, hostname, username, password):
        self.hostname = hostname
        self.username = username
        self.password = password

    def command(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.hostname, username=self.username, password=self.password)
        transport = ssh.get_transport()
        channel = transport.open_session()
        channel.exec_command('ifconfig;free;df -h')
        stdin, stdout, stderr = ssh.exec_command('ifconfig;free;df -h')
        log = stdout.read()
        print stderr.read()
        ssh.close()
        return log

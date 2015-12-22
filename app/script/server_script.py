#!/usr/bin/python
# coding=utf-8
#
# File Name: spark_script.py
# File Author: 姚丰利(lidey) 
# File Created Date: 2015-11-30 17:04
import paramiko


class ServerScript:
    def __init__(self, server):
        self.hostname = server.host
        self.username = server.name
        self.password = server.password

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=self.hostname, username=self.username, password=self.password)
        self.ssh = ssh

    def command(self, shell, timeout=10):
        stdin, stdout, stderr = self.ssh.exec_command(shell, timeout=timeout)
        return stdout.read(), stderr.read()

    def close(self):
        self.ssh.close()

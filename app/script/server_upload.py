#!/usr/bin/python
# coding=utf-8
import os
import datetime
import paramiko


class ServerUpload:
    def __init__(self, server):
        self.hostname = server.host
        self.username = server.name
        self.password = server.password
        self.remote_dir = server.path
        up = paramiko.Transport((self.hostname, 22))
        up.connect(username=self.username, password=self.password)
        sftp = paramiko.SFTPClient.from_transport(up)

        self.up = up
        self.sftp = sftp

    def upload(self, local_dir):
        files = os.listdir(local_dir)
        for f in files:
            if os.path.isfile(os.path.join(local_dir, f)):
                print 'Beginning to upload file %s ' % datetime.datetime.now()

                self.sftp.put(os.path.join(local_dir, f), os.path.join(self.remote_dir, f))

                print 'Upload file success %s ' % datetime.datetime.now()
            else:
                print '%s is not file' % f

    def close(self):
        self.up.close()

#!/usr/bin/python
# coding=utf-8
import os

import tornado
from tornado.web import stream_request_body
from app.core.base_handler import BaseHandler
from config import system


class UploadFileHandler(BaseHandler):
    def post(self):
        pass

    def get(self, url_first=''):
        upload_path = os.path.join(system['upload_file'], url_first)
        file = open(upload_path, 'rb')
        (_, filename) = os.path.split(file.name)
        self.set_header('Content-Type', 'application/octet-stream')
        upload_path.split()
        self.set_header('Content-Disposition', 'attachment; filename=' + filename)
        # 读取的模式需要根据实际情况进行修改
        buf_size = 4096
        with file as f:
            while True:
                data = f.read(buf_size)
                if not data:
                    break
                self.write(data)
        # 记得有finish哦
        self.finish()

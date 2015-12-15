#!/usr/bin/python
# coding=utf-8
import os

import tornado
from tornado.web import stream_request_body
from app.core.base_handler import BaseHandler


class UploadFileHandler(BaseHandler):

    def post(self):
        upload_path = os.path.join(os.path.dirname(__file__),'files')  # 文件的暂存路径
        if os.path.exists(upload_path):
            print('文件目录存在')
        else:
            os.makedirs(upload_path)
        file_metas = self.request.files['file']  # 提取表单中‘name’为‘file’的文件元数据
        for meta in file_metas:
            filename = meta['filename']
            filepath = os.path.join(upload_path, filename)
            with open(filepath, 'wb') as up:  # 有些文件需要已二进制的形式存储，实际中可以更改
                up.write(meta['body'])
        self.write({'answer': 'finished!'})

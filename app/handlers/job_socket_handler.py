#!/usr/bin/python
# coding=utf-8

import tornado.websocket
from app.model.job_progress_model import JobProgress


class JobSocketHandler(tornado.websocket.WebSocketHandler):
    clients = set()
    flag = True
    @staticmethod
    def send_to_all(message):
        for c in JobSocketHandler.clients:
            c.write_message(message)

    def open(self):
        JobSocketHandler.clients.add(self)
        list = JobProgress.select().where(JobProgress.status == 1)
        print len(list)
        if len(list)>0:
            resp = []
            for data in list:
                resp.append(data.to_dict())
            self.write_message({'type': 'all', 'list': resp})
        else:
            self.write_message({'type': 'all', 'list': []})
        print "打开连接"

    def on_close(self):
        JobSocketHandler.clients.remove(self)
        print "关闭连接"
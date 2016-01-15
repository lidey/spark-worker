#!/usr/bin/python
# coding=utf-8
#
# File Name: base_thread.py
# File Author: 姚丰利(lidey) 
# File Created Date: 2016-01-15 10:46
import threading

from tornado.websocket import WebSocketClosedError


class WebSocketThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(WebSocketThread, self).__init__(*args, **kwargs)

    def run(self):
        try:
            super(WebSocketThread, self).run()
        except WebSocketClosedError:
            pass

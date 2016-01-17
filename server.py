#!/usr/bin/python
# coding=utf-8
# Filename: server.py
import logging

import tornado.ioloop
import config
from application import application

peewee_log = logging.getLogger('peewee')
peewee_log.setLevel(config.logger['level'])
peewee_log.addHandler(logging.StreamHandler())
# access_log = logging.getLogger("tornado.access")
# app_log = logging.getLogger("tornado.application")
# app_log.setLevel(config.logger['level'])
# gen_log = logging.getLogger("tornado.general")
# gen_log.setLevel(config.logger['level'])

application.listen(config.system['port'])

print 'Development server is running at http://%s:%s/' % (config.system['hostname'], config.system['port'])
print 'Quit the server with CONTROL-C'
tornado.ioloop.IOLoop.instance().start()

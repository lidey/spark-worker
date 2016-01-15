#!/usr/bin/python
# coding=utf-8
#
# File Name: router.py.py
# File Author: lidey 
# File Created Date: 2015-11-27 12:47
from app.handlers.database_handler import DatabaseHandler
from app.handlers.job_socket_handler import JobSocketHandler
from app.handlers.spark_handler import SparkHandler, SparkTerminalHandler
from app.handlers.upload_file_handler import UploadFileHandler
from app.handlers.job_handler import JobHandler
from app.handlers.job_progress_handler import JobProgressHandler
from app.handlers.scheduler_handler import SchedulerHandler
from app.handlers.script_handler import ScriptHandler
from app.handlers.server_handler import ServerHandler, WebTerminalHandler, WebTerminalKillHandler
from app.handlers.user_handler import UserHandler
from app.handlers.index_handler import MainHandler

urls = [
    (r"/", MainHandler, dict()),
    (r"/user/(.*)", UserHandler, dict()),
    (r"/job/(.*)", JobHandler, dict()),
    (r"/server/(.*)", ServerHandler, dict()),
    (r'/terminal', WebTerminalHandler, dict()),
    (r'/terminal/kill', WebTerminalKillHandler, dict()),
    (r"/script/(.*)", ScriptHandler, dict()),
    (r"/scheduler/(.*)", SchedulerHandler, dict()),
    (r"/process/(.*)", JobProgressHandler, dict()),
    (r"^/upload_file/(.*)$", UploadFileHandler, dict()),
    (r"/job-socket", JobSocketHandler, dict()),
    (r"/database/(.*)/(.*)", DatabaseHandler, dict()),
    (r"/database/(.*)", DatabaseHandler, dict()),
    (r"/spark/(.*)/(.*)", SparkHandler, dict()),
    (r"/spark/(.*)", SparkHandler, dict()),
    (r'/terminal/spark', SparkTerminalHandler, dict()),
]

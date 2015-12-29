#!/usr/bin/python
# coding=utf-8
#
# File Name: base_exception.py
# File Author: 姚丰利(lidey) 
# File Created Date: 2015-12-28 13:39


class ConnectException(Exception):
    def __init__(self, e):
        self.message = e.args[1]

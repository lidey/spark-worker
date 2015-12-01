#!/usr/bin/python
# coding=utf-8
#
# File Name: tools.py.py
# File Author: lidey 
# File Created Date: 2015-11-27 12:51
import uuid
import random
import time
import hashlib


def md5(instr):
    return hashlib.md5(instr.encode('utf-8')).hexdigest()


def timestamp():
    return int(time.time())


def format_year(indate):
    # uu = datetime.datetime.strptime(indate,'%a, %d %b %Y %H:%M:%S')
    return indate.strftime('%m-%d')


def format_date(indate):
    return indate.strftime('%Y-%m-%d %H:%M:%S')


def get_uuid():
    return str(uuid.uuid1())


def get_uu8d():
    return str(uuid.uuid1()).split('-')[0]


def get_uu4d():
    sel_arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    slice = random.sample(sel_arr, 4)
    return ''.join(slice)


def get_uu5d():
    sel_arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    slice = random.sample(sel_arr, 5)
    return ''.join(slice)


def get_uudd(lenth):
    sel_arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    slice = random.sample(sel_arr, lenth)
    while slice[0] == '0':
        slice = random.sample(sel_arr, lenth)
    return int(''.join(slice))


def get_uu6d():
    sel_arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
    slice = random.sample(sel_arr, 6)
    return ''.join(slice)

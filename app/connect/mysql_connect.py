#!/usr/bin/python
# coding=utf-8
#
# File Name: mysql_connect.py
# File Author: 姚丰利(lidey) 
# File Created Date: 2015-12-28 11:40
import pymysql
from pymysql.err import OperationalError

from app.core.base_exception import ConnectException


class MysqlConnect:
    """
    mysql数据操作类
    """

    def __init__(self, database):
        try:
            self.connect = pymysql.connect(host=database.hostname, port=database.port,
                                           user=database.username,
                                           passwd=database.password,
                                           db=database.name)
        except OperationalError, e:
            raise ConnectException(e)

    def get_connect(self):
        return self.connect

    def get_tables(self, search):
        """
        根据关键字查询数据库表
        :param search:过滤关键字
        :return:数据表
        """
        cur = self.connect.cursor()
        sql = 'show tables like %s'
        cur.execute(sql, ('%' + search + '%'))
        tables = list()
        for r in cur.fetchall():
            tables.append(r[0])
        cur.close()
        return tables

    def get_columns(self, table):
        """
        根据数据库表名查询表结构
        :param table: 数据库表名
        :return: 表结构
        """
        cur = self.connect.cursor()
        cur.execute('show columns from ' + table)
        columns = list()
        for r in cur.fetchall():
            column = dict()
            column['field'] = r[0]
            column['type'] = r[1]
            column['null'] = r[2]
            column['key'] = r[3]
            column['default'] = r[4]
            columns.append(column)
        cur.close()
        return columns

    def test(self):
        """
        测试数据库链接
        """
        cur = self.connect.cursor()
        cur.execute('select 1')
        cur.fetchone()
        cur.close()

    def close(self):
        self.connect.close()

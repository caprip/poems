# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-12-29 07:08:09
# @Author  : PinG (y.p@qq.com)
# @Link    : http://zhangyunping.cn
# @Version : $Id$

import datetime
import json
import sqlite3


class dao():
    def __init__(self, database):
        self.__database = database
        conn = sqlite3.connect(self.__database)
        conn.commit()
        conn.close()

    def create_table(self, tabledict):
        sqlbase = 'CREATE TABLE IF NOT EXISTS {}({})'
        structure = []
        for each in tabledict['structure']:
            structure.append(' '.join(each))
        conn = sqlite3.connect(self.__database)
        sql = sqlbase.format(tabledict['tablename'], ','.join(structure))
        result = conn.execute(sql)
        conn.commit()
        conn.close()
        return result

    def insert_values(self, valuesdict, autoincrement=False):
        sqlbase = 'INSERT INTO {} VALUES ({})'
        cols = ['?'] * len(valuesdict['values'][0])
        if autoincrement:
            cols = ['NULL'] + cols
        sql = sqlbase.format(valuesdict['table'], ','.join(cols))
        conn = sqlite3.connect(self.__database)
        result = conn.executemany(sql, valuesdict['values'])
        conn.commit()
        conn.close()
        return result

    def replace_values(self, valuesdict, autoincrement=False):
        sqlbase = 'REPLACE INTO {} VALUES ({})'
        cols = ['?'] * len(valuesdict['values'][0])
        if autoincrement:
            cols = ['NULL'] + cols
        sql = sqlbase.format(valuesdict['table'], ','.join(cols))
        conn = sqlite3.connect(self.__database)
        result = conn.executemany(sql, valuesdict['values'])
        conn.commit()
        conn.close()
        return result

    def select_values(self, selectdict):
        sqlbase = 'SELECT * FROM {}'
        keys = []
        for each in selectdict['keys']:
            if each[2].upper() == 'LIKE':
                keys.append('{} {} "%{}%"'.format(each[0], each[2], each[1]))
            else:
                keys.append('{} {} "{}"'.format(each[0], each[2], each[1]))
        sql = sqlbase.format(selectdict['table'])
        if len(keys) > 0:
            sql += ' WHERE ' + ' and '.join(keys)
        conn = sqlite3.connect(self.__database)
        result = conn.execute(sql).fetchall()
        conn.close()
        return result

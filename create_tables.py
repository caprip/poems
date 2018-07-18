#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-07-17 13:49:54
# @Author  : PinG (y.p@qq.com)
# @Link    : http://zhangyunping.cn
# @Version : $Id$

import sqlite3

DATABASE_FILE = 'poems.db'


def create_tables():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.execute('CREATE TABLE poems(\
        poem_uuid TEXT PRIMARY KEY,\
        poem_title TEXT,\
        poem_author TEXT,\
        poem_dynasty TEXT,\
        poem_content TEXT\
        )')
    conn.execute('CREATE TABLE checkin(\
        checkin_day TEXT PRIMARY KEY,\
        checkin_uuid TEXT\
        )')
    conn.commit()
    conn.close()


create_tables()

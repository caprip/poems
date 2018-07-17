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
    conn.execute('CREATE TABLE writers(\
        writer_id,\
        writer_name,\
        writer_nickname,\
        writer_dynasty,\
        writer_url\
        )')
    conn.execute('CREATE TABLE poems(\
        poem_id,\
        poem_writer,\
        poem_type,\
        poem_content,\
        poem_url\
        )')
    conn.execute('CREATE TABLE lists(\
        list_id,\
        list_creator,\
        list_poems,\
        list_total_visits,\
        list_daily_visits,\
        list_novisitd_days\
        )')
    conn.commit()
    conn.close()

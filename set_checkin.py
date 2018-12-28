# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-12-28 12:15:18
# @Author  : PinG (y.p@qq.com)
# @Link    : http://zhangyunping.cn
# @Version : $Id$

import datetime
import json
import sqlite3
import uuid

import requests
import xlrd
from bs4 import BeautifulSoup

DATABASE_CHECKIN = 'checkin.db'
TABLE_CHECKINLIST = 'checkinlist'
XLSX_FILE = 'sczl.xlsx'


def create_checkinlist_table(table_checkinlist):
    conn = sqlite3.connect(DATABASE_CHECKIN)
    result = conn.execute('CREATE TABLE {}(\
        checkinlist_index INTEGER PRIMARY KEY AUTOINCREMENT,\
        checkinlist_name TEXT,\
        checkinlist_date TEXT,\
        checkinlist_days TEXT\
        )'.format(table_checkinlist))
    conn.commit()
    conn.close()
    return result


def create_checkin_table(table_checkin):
    conn = sqlite3.connect(DATABASE_CHECKIN)
    result = conn.execute('CREATE TABLE {}(\
        checkin_index INTEGER PRIMARY KEY AUTOINCREMENT,\
        checkin_day TEXT,\
        checkin_uuid TEXT,\
        checkin_url TEXT\
        )'.format(table_checkin))
    conn.commit()
    conn.close()
    return result


def is_checkinlist_exist(checkinlist_name):
    result = False
    conn = sqlite3.connect(DATABASE_CHECKIN)
    if len(conn.execute('SELECT * FROM {} WHERE checkinlist_name="{}"'
                        .format(TABLE_CHECKINLIST, checkinlist_name))
           .fetchall()) > 0:
        result = True
    conn.close()
    return result


def create_checkinlist(checkinlist_name, checkinlist_days=0):
    result = False
    create_date = datetime.date.today().strftime('%Y%m%d')
    if create_checkin_table(checkinlist_name):
        conn = sqlite3.connect(DATABASE_CHECKIN)
        result = conn.execute('INSERT INTO {} VALUES (NULL,?,?,?)'
                              .format(TABLE_CHECKINLIST),
                              [checkinlist_name,
                               create_date,
                               checkinlist_days])
        conn.commit()
        conn.close()
    return result


def get_checkin_from_xlsx(filepath):
    xlsfile = xlrd.open_workbook(filepath)
    for eachsheet in xlsfile.sheets():
        if not is_checkinlist_exist(eachsheet.name):
            create_checkinlist(eachsheet.name, eachsheet.nrows)
    return

# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-12-29 17:00:00
# @Author  : PinG (y.p@qq.com)
# @Link    : http://zhangyunping.cn
# @Version : $Id$

from dao_sqlite3 import dao

DB_checkin = 'checkin.db'
CHECKINLIST_structure = {
    'tablename': 'checkinlist',
    'structure': [
        ['checkinlist_table', 'TEXT PRIMARY KEY'],
        ['checkinlist_name', 'TEXT']
    ]
}
CHECKIN_structure = {
    'tablename': '',
    'structure': [
        ['checkin_date', 'TEXT PRIMARY KEY'],
        ['checkin_poem', 'TEXT'],
        ['checkin_info', 'TEXT']
    ]
}


class checkindao(dao):
    def __init__(self):
        dao.__init__(self, DB_checkin)
        self.create_table(CHECKINLIST_structure)

    def is_checkinlist_exist(self, table):
        select = {
            'table': CHECKINLIST_structure['tablename'],
            'keys': [
                ['checkinlist_table', table, '=']
            ]
        }
        return len(self.select_values(select)) > 0

    def get_checkin_name(self, table):
        select = {
            'table': CHECKINLIST_structure['tablename'],
            'keys': [
                ['checkinlist_table', table, '=']
            ]
        }
        return self.select_values(select)[0][1]

    def find_checkin(self, table, checkindate):
        select = {
            'table': table,
            'keys': [
                ['checkin_date', checkindate, '=']
            ]
        }
        return self.select_values(select)

    def save_checkinlist(self, checkinlist):
        structure = CHECKIN_structure.copy()
        structure['table'] = checkinlist['table']
        replacelist = {
            'table': CHECKINLIST_structure['tablename'],
            'values': [
                [checkinlist['table'], checkinlist['name']]
            ]
        }
        self.create_table(structure)
        self.replace_values(replacelist)
        return self.replace_values(checkinlist)

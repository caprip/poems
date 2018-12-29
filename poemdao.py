# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-12-29 13:23:33
# @Author  : PinG (y.p@qq.com)
# @Link    : http://zhangyunping.cn
# @Version : $Id$

import uuid

from dao_sqlite3 import dao

DB_poems = 'poems.db'
POEMS_structure = {
    'tablename': 'poems',
    'structure': [
        ['poem_uuid', 'TEXT PRIMARY KEY'],
        ['poem_title', 'TEXT'],
        ['poem_author', 'TEXT'],
        ['poem_dynasty', 'TEXT'],
        ['poem_content', 'TEXT']
    ]
}


class poemdao(dao):
    def __init__(self):
        dao.__init__(self, DB_poems)
        self.create_table(POEMS_structure)

    def find(self, keyname, keyword, operator='='):
        select = {
            'table': POEMS_structure['tablename'],
            'keys': [
                [keyname, keyword, operator]
            ]
        }
        return self.select_values(select)

    def find_uuid(self, keyword):
        return self.find('poem_uuid', keyword)

    def find_title(self, keyword, operator='='):
        return self.find('poem_title', keyword, operator)

    def find_author(self, keyword):
        return self.find('poem_author', keyword)

    def find_content(self, keyword):
        return self.find('poem_content', keyword, 'LIKE')

    def find_poem(self, keyword):
        result = ''
        try:
            uuid.UUID(keyword)
            temp = self.find_uuid(keyword)
        except:
            temp = self.find_title(keyword)
            if len(temp) == 0:
                temp = self.find_title(keyword, 'LIKE')
            if len(temp) == 0:
                temp = self.find_content(keyword)
        if len(temp) > 0:
            result = temp
        return result

    def is_uuid_exist(self, keyword):
        return len(self.find_uuid(keyword)) > 0

    def is_poem_exist(self,keyword):
        return len(self.find_poem(keyword)) > 0

    def save_poem(self, poem):
        insert = {
            'table': POEMS_structure['tablename'],
            'values': [
                poem,
            ]
        }
        self.insert_values(insert)

    def save_poems(self, poems):
        insert = {
            'table': POEMS_structure['tablename'],
            'values': poems
        }
        self.insert_values(insert)

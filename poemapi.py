# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-12-28 20:20:20
# @Author  : PinG (y.p@qq.com)
# @Link    : http://zhangyunping.cn
# @Version : $Id$

import json
import sqlite3
import uuid

import requests
from bs4 import BeautifulSoup
from dao_sqlite3 import dao

URL_baidu = 'http://www.baidu.com/s'
URL_baiduhanyu = 'https://hanyu.baidu.com/shici/detail'
KEY_site = ' site:hanyu.baidu.com'

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

DB_checkin = 'checkin.db'
CHECKINLIST_structure = {
    'tablename': 'checkinlist',
    'structure': [
        ['checkinlist_table', 'TEXT PRIMARY KEY'],
        ['checkinlist_name', 'TEXT']
    ]
}
CHECKIN_structure = {
    'tablename': '{}',
    'structure': [
        ['checkin_date', 'TEXT PRIMARY KEY'],
        ['checkin_poem', 'TEXT'],
        ['checkin_info', 'TEXT']
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

    def is_poem_exist(self, keyword):
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


class poem:
    def __init__(self, keyword):
        self.__uuid = ''
        self.__title = ''
        self.__author = ''
        self.__dynasty = ''
        self.__content = ''
        self.__keyword = keyword
        if not self.__get_poem_db():
            self.__get_poem_web()

    def __get_poem_db(self):
        temp = poemdao().find_poem(self.__keyword)
        result = len(temp) > 0
        if result:
            self.__uuid = temp[0][0]
            self.__title = temp[0][1]
            self.__author = temp[0][2]
            self.__dynasty = temp[0][3]
            self.__content = temp[0][4]
        return result

    def __get_poem_web(self):
        try:
            uuid.UUID(self.__keyword)
            self.__uuid = keyword
        except:
            self.__get_uuid_with_keyword()
        self.__get_poem_with_uuid()

    def __get_uuid_with_keyword(self):
        payload = {'wd': self.__keyword + KEY_site}
        res = requests.get(URL_baidu, params=payload)
        soup = BeautifulSoup(res.text, 'html5lib')
        result = []
        k = 0
        while len(result) == 0:
            url_temp = soup(class_='result c-container ')[k].h3.a['href']
            res_temp = requests.get(url_temp)
            if URL_baiduhanyu in res_temp.url:
                result.append(res_temp.url)
            k += 1
        self.__uuid = result[0][41:73]

    def __get_poem_with_uuid(self):
        payload = {'pid': self.__uuid}
        res = requests.get(URL_baiduhanyu, params=payload)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, 'html5lib')
        self.__title = soup.h1.text
        html_author = soup(class_='poem-detail-header-author')
        self.__author = html_author[0].text.strip()[4:]
        self.__dynasty = html_author[1].text.strip()[4:]
        html_content = soup(class_='poem-detail-main-text')
        poem_content = []
        for eachline in html_content:
            if html_content.index(eachline) % 2 == 0:
                poem_content.append(eachline.text.strip())
        self.__content = json.dumps(poem_content, ensure_ascii=False)

    def uuid(self):
        return self.__uuid

    def title(self):
        return self.__title

    def author(self):
        return self.__author

    def dynasty(self):
        return self.__dynasty

    def content(self):
        return self.__content

    def exportdict(self):
        return {
            'uuid': self.__uuid,
            'title': self.__title,
            'author': self.__author,
            'dynasty': self.__dynasty,
            'content': self.__content
        }

    def exportlist(self):
        return [
            self.__uuid,
            self.__title,
            self.__author,
            self.__dynasty,
            self.__content
        ]

    def saveindb(self):
        poem = [
            self.__uuid,
            self.__title,
            self.__author,
            self.__dynasty,
            self.__content
        ]
        if not poemdao().is_uuid_exist(self.__uuid):
            return poemdao().save_poem(poem)

    def get_uuid_db(self):
        self.saveindb()
        return self.uuid()


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
        structure['tablename'] = checkinlist['table']
        replacelist = {
            'table': CHECKINLIST_structure['tablename'],
            'values': [
                [checkinlist['table'], checkinlist['name']]
            ]
        }
        self.create_table(structure)
        self.replace_values(replacelist)
        return self.replace_values(checkinlist)


class checkin(checkindao):
    def __init__(self, checkinlist=''):
        pass

    def __get_checkin_db(self):
        pass

    def __set_checkin(self, checkindict):
        pass

    def getuuid(self, checkindate):
        pass

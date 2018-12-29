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

from poemdao import poemdao

URL_baidu = 'http://www.baidu.com/s'
URL_baiduhanyu = 'https://hanyu.baidu.com/shici/detail'
KEY_site = ' site:hanyu.baidu.com'


class poem:
    def __init__(self, keyword):
        self.__keyword = keyword
        if not self.__get_poem_db():
            self.__get_poem_web()

    def __get_poem_db(self):
        temp = poemdao().find_poem(self.__keyword)
        result = len(temp) > 0
        if result:
            self.__uuid,
            self.__title,
            self.__author,
            self.__dynasty,
            self.__content = temp[0]
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

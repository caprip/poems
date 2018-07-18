#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-07-17 13:49:54
# @Author  : PinG (y.p@qq.com)
# @Link    : http://zhangyunping.cn
# @Version : $Id$

import sqlite3
import requests
from bs4 import BeautifulSoup

DATABASE_FILE = 'poems.db'
URL_baiduhanyu = 'https://hanyu.baidu.com/shici/detail'


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


def get_poems(poem_id):
    preload = {'pid': poem_id}
    res_baiduhanyu = requests.get(URL_baiduhanyu, params=preload)
    res_baiduhanyu.encoding = 'utf-8'
    soup = BeautifulSoup(res_baiduhanyu.text, 'html5lib')
    poem_title = soup.h1.text
    # print(soup.find_all(class_='poem-detail-header-author'))
    html_author = soup(class_='poem-detail-header-author')
    poem_author = html_author[0].text.strip()[4:]
    poem_dynasty = html_author[1].text.strip()[4:]
    html_content = soup(class_='poem-detail-main-text')
    poem_content = []
    for eachline in html_content:
        if html_content.index(eachline) % 2 == 0:
            poem_content += [(eachline.text.strip())]
    print(poem_title)
    print(poem_author, poem_dynasty)
    print(poem_content)


def get_poems2(keyword):
    preload = {'wd': keyword}
    res_baiduhanyu = requests.get('https://hanyu.baidu.com/s', params=preload)
    res_baiduhanyu.encoding = 'utf-8'
    soup = BeautifulSoup(res_baiduhanyu.text, 'html5lib')
    print(res_baiduhanyu.url)
    print(soup)
    '''
    >>> r.text.find('"url":"http')
196528
>>> t=r.text[196528:]
>>> t.find('}')
166
>>> t=t[:166]
>>> t
'"url":"http://www.baidu.com/link?url=wsM2TT1qV78oE0-4Yi9Xv2i7fEb6HqJh_7nFf7cgyvCvEN_sXNx8Uisk7VwieGBCRsw6W45-82qhsC-XOxUouEizTUVfyPJR-u7vlQ76XseU8L66gNwbqwyqofdxk0_J"'
>>> t[t.find('http'):-1]
'http://www.baidu.com/link?url=wsM2TT1qV78oE0-4Yi9Xv2i7fEb6HqJh_7nFf7cgyvCvEN_sXNx8Uisk7VwieGBCRsw6W45-82qhsC-XOxUouEizTUVfyPJR-u7vlQ76XseU8L66gNwbqwyqofdxk0_J'
>>> rr=requests.get(t[7:-1])
>>> rr
<Response [200]>
>>> rr.url
'https://hanyu.baidu.com/shici/detail?pid=64a28ff1f75b44b791d7af5cd85c0495'
>>> rr.url[-32:]
'64a28ff1f75b44b791d7af5cd85c0495'
    '''


# get_poems('ba9e4875904f4e8887d691f6a753d5f4')
get_poems('35146e25078b4a3585179d31caa2bc29')
get_poems2('山居秋暝')

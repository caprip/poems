#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-07-18 18:18:18
# @Author  : PinG (y.p@qq.com)
# @Link    : http://zhangyunping.cn
# @Version : $Id$

import datetime
import json
import sqlite3
import uuid
import requests
from bs4 import BeautifulSoup

DATABASE_FILE = 'poems.db'


def get_details(res_text):
    soup = BeautifulSoup(res_text, 'html5lib')
    poem_title = soup.h1.text
    html_author = soup(class_='poem-detail-header-author')
    poem_author = html_author[0].text.strip()[4:]
    poem_dynasty = html_author[1].text.strip()[4:]
    html_content = soup(class_='poem-detail-main-text')
    poem_content = []
    for eachline in html_content:
        if html_content.index(eachline) % 2 == 0:
            poem_content.append(eachline.text.strip())
    return poem_title, poem_author, poem_dynasty, json.dumps(poem_content, ensure_ascii=False)


def get_poem_with_pid(poem_uuid):
    URL_baiduhanyu = 'https://hanyu.baidu.com/shici/detail'
    payload = {'pid': poem_uuid}
    res_poem = requests.get(URL_baiduhanyu, params=payload)
    res_poem.encoding = 'utf-8'
    details = get_details(res_poem.text)
    return (poem_uuid,) + details


def get_url_from_baidu(keyword):
    URL_baidu = 'http://www.baidu.com/s'
    payload = {'wd': keyword}
    res_baidu = requests.get(URL_baidu, params=payload)
    soup = BeautifulSoup(res_baidu.text, 'html5lib')
    return soup(class_='result c-container ')[0].h3.a['href']
    '''
    TAG_start = '"url":"http'
    TAG_end = '}'
    t = res_baidu.text
    return t[t.find(TAG_start) + 7:t.find(TAG_end, t.find(TAG_start)) - 1]'''


def get_poem_from_url(url_poem):
    SIGN_baiduwenku = 'https://hanyu.baidu.com/shici/detail'
    res_poem = requests.get(url_poem)
    res_poem.encoding = 'utf-8'
    if SIGN_baiduwenku in res_poem.url:
        poem_uuid = res_poem.url[41:73]
        details = get_details(res_poem.text)
        return (poem_uuid,) + details
    else:
        return 'URL ERROR:' + res_poem.url


def get_poem_with_key(keyword):
    try:
        uuid.UUID(keyword)
        poem = get_poem_with_pid(keyword)
    except:
        url_poem = get_url_from_baidu(keyword + ' 百度汉语')
        poem = get_poem_from_url(url_poem)
    return poem


def save_poem(poem):
    conn = sqlite3.connect(DATABASE_FILE)
    conn.execute('INSERT INTO poems VALUES (?,?,?,?,?)', poem)
    conn.commit()
    conn.close()


def list_all_poems(columns='*'):
    conn = sqlite3.connect(DATABASE_FILE)
    result = conn.execute('SELECT {} FROM poems'.format(columns)).fetchall()
    conn.close()
    return result


def create_dates(yy, mm, dd, days,):
    dates = []
    for i in range(days):
        dates.append((datetime.date(yy, mm, dd) +
                      datetime.timedelta(i)).strftime('%Y%m%d'))
    return dates


def set_checkin(filepath, datestart=''):
    if datestart == '':
        datestart = datetime.date.today().strftime('%Y%m%d')
    with open(filepath) as fp:
        uuids = json.load(fp, encoding='utf-8')
    tablecheckin = []
    '''
    for i in range(len(uuids)):
        tablecheckin.append(((datetime.datetime.strptime(datestart, '%Y%m%d') +
                       datetime.timedelta(i)).strftime('%Y%m%d'), uuids[i]))
    '''
    for each in uuids:
        tablecheckin.append(((datetime.datetime.strptime(datestart, '%Y%m%d') +
                              datetime.timedelta(uuids.index(each))).strftime('%Y%m%d'), each))
    conn = sqlite3.connect(DATABASE_FILE)
    result = conn.executemany('INSERT INTO checkin VALUES (?,?)', tablecheckin)
    conn.commit()
    conn.close()
    return result


def get_save_and_set(filepath, datestart=''):
    if datestart == '':
        datestart = datetime.date.today().strftime('%Y%m%d')
    with open(filepath) as fp:
        keys = json.load(fp, encoding='utf-8')
    tablepoems, tablecheckin = [], []
    for each in keys:
        print(each)
        poem = get_poem_with_key(each)
        tablepoems.append(poem)
        tablecheckin.append(((datetime.datetime.strptime(datestart, '%Y%m%d') +
                              datetime.timedelta(keys.index(each))).strftime('%Y%m%d'), poem[0]))
    print(tablepoems)
    print(tablecheckin)
    conn = sqlite3.connect(DATABASE_FILE)
    result = []
    result.append(conn.executemany(
        'INSERT INTO poems VALUES (?,?,?,?,?)', tablepoems))
    result.append(conn.executemany(
        'INSERT INTO checkin VALUES (?,?)', tablecheckin))
    conn.commit()
    conn.close()
    return result


if __name__ == '__main__':
    print('This is get_poems.py!\n')
    # print(get_save_and_set('list201811w4.json'))
    print(get_save_and_set('list201811w5.json', '20181127'))
    # print(get_poem_with_key('长安秋望'))
    # print(set_checkin('checkin1.json', 2018, 7, 17, 30))
    '''
    sql_result = list_all_poems()
    all_uuids = []
    for each in sql_result:
        all_uuids.append(each[0])
    # with open('checkin1.json', 'w') as fp:
        # json.dump(all_uuids, fp, indent=4)
    print(all_uuids)'''
    # get_poem_with_pid('ba9e4875904f4e8887d691f6a753d5f4')
    # get_poem_with_pid('35146e25078b4a3585179d31caa2bc29')
    # print(get_poem_with_key('a20ccf16278df7ec4df2f965624423b1'))
    # print(get_poem_with_key('山居秋暝 百度汉语'))
    '''
    with open('poemlist1.txt') as fp:
        for eachline in fp.readlines():
            poem = get_poem_with_key(eachline)
            save_poem(poem)
    '''

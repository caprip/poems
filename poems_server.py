#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-07-22 17:18:23
# @Author  : PinG (y.p@qq.com)
# @Link    : http://zhangyunping.cn
# @Version : $Id$

import json
import random
from bottle import route, run
import sqlite3

DATABASE_FILE = 'poems.db'


def get_poem_from_db(author, title):
    conn = sqlite3.connect(DATABASE_FILE)
    result = conn.execute(
        'SELECT * FROM poems WHERE poem_author=(?) AND poem_title=(?)', (author, title)).fetchall()
    conn.close()
    return result[0]


def get_random_poem_from_db():
    conn = sqlite3.connect(DATABASE_FILE)
    result = conn.execute('SELECT * FROM poems').fetchall()
    conn.close()
    return random.choice(result)


def create_html_poem(poem):
    html_title = '<title>' + poem[1] + '-' + poem[2] + '</title>'
    html_h1 = '<h1>' + poem[1] + '</h1>'
    html_h2 = '<h2>' + poem[3] + ' ' + poem[2] + '</h2>'
    html_p = '<p>' + '</p><p>'.join(json.loads(poem[4])) + '</p>'
    return html_title + html_h1 + html_h2 + html_p


@route('/p/<author>/<title>')
def http_poem(author, title):
    poem = get_poem_from_db(author, title)
    return create_html_poem(poem)


@route('/random')
def http_random():
    poem = get_random_poem_from_db()
    return create_html_poem(poem)


run(host='localhost', port=8080)

#print(get_poem_from_db('贾岛', '题李凝幽居'))

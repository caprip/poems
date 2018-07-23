#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-07-22 17:18:23
# @Author  : PinG (y.p@qq.com)
# @Link    : http://zhangyunping.cn
# @Version : $Id$

import time
import json
import random
from bottle import route, run
import sqlite3

DATABASE_FILE = 'poems.db'
URL_poem_mp3 = 'http://app.dict.baidu.com/static/shici_mp3/{}.mp3'


def get_poem_from_db(uuid='', author='', title=''):
    params = 'WHERE'
    if len(uuid) > 0:
        params += ' poem_uuid="{}"'.format(uuid)
    if len(author) > 0:
        if len(params) > 5:
            params += ' AND'
        params += ' poem_author="{}"'.format(author)
    if len(title) > 0:
        if len(params) > 5:
            params += ' AND'
        params += ' poem_title="{}"'.format(title)
    if params == 'WHERE':
        params = ''
    conn = sqlite3.connect(DATABASE_FILE)
    result = conn.execute('SELECT * FROM poems {}'.format(params)).fetchall()
    conn.close()
    return result[0]


def get_random_poem_from_db():
    conn = sqlite3.connect(DATABASE_FILE)
    result = conn.execute('SELECT * FROM poems').fetchall()
    conn.close()
    return random.choice(result)


def create_html_poem(poem):
    html = '<title>{}-{}</title>'.format(poem[1], poem[2])
    html += '<body align="center" style="line-height:66%">'
    html += '<audio src="{}" controls="controls"></audio>'.format(
        URL_poem_mp3.format(poem[0]))
    html += '<h3>{}</h3>'.format(poem[1])
    html += '<h5>{} {}</h5>'.format(poem[3], poem[2])
    html += '<p>{}</p>'.format('</p><p>'.join(json.loads(poem[4])))
    html += '''<script>function resizefont()
        {document.body.style.fontSize=window.innerWidth/25+"px";}
        window.onload=resizefont;
        window.onresize=resizefont;
        </script>'''
    html += '</body>'
    return html


def create_html_recite(poem):
    html = '<title>{}-{}</title>'.format(poem[1], poem[2])
    html += '<body align="center" style="line-height:66%" onclick="echoauthor()" ondblclick="echopoem()">'
    html += '<audio id="audio" src="{}" controls="controls" style="visibility:hidden"></audio>'.format(
        URL_poem_mp3.format(poem[0]))
    html += '<h3 id="title">{}</h3>'.format(poem[1])
    html += '<h5 id="author" style="visibility:hidden">{} {}</h5>'.format(
        poem[3], poem[2])
    html += '<div id="content" style="visibility:hidden">'
    html += '<p>{}</p>'.format('</p><p>'.join(json.loads(poem[4])))
    html += '</div>'
    html += '''<script>function resizefont(){document.body.style.fontSize=window.innerWidth/25+"px";}
        function echoauthor(){document.getElementById('author').style.visibility="visible";}
        function echopoem(){document.getElementById('audio').style.visibility="visible";
        document.getElementById('content').style.visibility="visible";}
        window.onload=resizefont;window.onresize=resizefont;</script>'''
    html += '</body>'
    return html


def get_checkin_uuid(checkinday):
    conn = sqlite3.connect(DATABASE_FILE)
    checkin_uuid = conn.execute(
        'SELECT checkin_uuid FROM checkin WHERE checkin_day=(?)', (checkinday,)).fetchall()
    conn.close()
    return checkin_uuid


@route('/p/<author>/<title>')
def http_poem(author, title):
    poem = get_poem_from_db(author=author, title=title)
    return create_html_poem(poem)


@route('/random')
def http_random():
    poem = get_random_poem_from_db()
    return create_html_poem(poem)


@route('/checkin')
@route('/checkin/<checkinday>')
def http_checkin(checkinday=time.strftime('%Y%m%d')):
    checkin_uuid = get_checkin_uuid(checkinday)
    if len(checkin_uuid) == 1:
        poem = get_poem_from_db(uuid=checkin_uuid[0][0])
        return create_html_poem(poem)
    else:
        return '打卡信息有误。'


@route('/recite')
def http_recite():
    poem = get_random_poem_from_db()
    return create_html_recite(poem)


run(host='0.0.0.0', port=80)

#print(get_poem_from_db('贾岛', '题李凝幽居'))

# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-12-28 12:15:18
# @Author  : PinG (y.p@qq.com)
# @Link    : http://zhangyunping.cn
# @Version : $Id$

import xlrd

from poemapi import checkindao, poem

FILE_xlsx = 'sczl.xlsx'
SHEET_menu = 'CheckinList'


def set_checkinlist_from_xlsx(filepath):
    workbook = xlrd.open_workbook(filepath)
    sheetmenu = workbook.sheet_by_name(SHEET_menu)
    checkins = []
    for eachsheet in range(sheetmenu.nrows):
        templist = []
        sheetrow = sheetmenu.row_values(eachsheet)
        sheet = workbook.sheet_by_name(sheetrow[0])
        for each in range(sheet.nrows):
            eachrow = sheet.row_values(each)
            eachrow[1] = poem(eachrow[1]).get_uuid_db()
            templist.append(eachrow)
        checkin = {}
        checkin['sheet'] = sheetrow[0]
        checkin['table'] = sheetrow[1]
        checkin['name'] = sheetrow[2]
        checkin['values'] = templist
        checkins.append(checkin)
    for each in checkins:
        checkindao().save_checkinlist(each)
        # print(each)


if __name__ == '__main__':
    print('This is set_checkin.py!\n')
    set_checkinlist_from_xlsx(FILE_xlsx)
    print('Done.\n')

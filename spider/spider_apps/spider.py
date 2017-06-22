#!/usr/bin/env python
# -*- coding: utf_8 -*-

import sys
from downloader import Downloader
from configs.mylog import MyLog
import xlrd
import time
import database
import os
import test


def start_spider():
    '''
    start spider
    :return: 
    '''
    download = Downloader()
    try:
        _my_log_.info('starting spider')
        # get swift code from the excel
        data = xlrd.open_workbook('./excel/交通银行代理行总部清单.xlsx')
        sheet = data.sheet_by_index(0)
        sheet.col_values(0, 1)


        urls = ['ARABAU2S']
        # for code in sheet.col_values(0):
        for code in urls:
            date_now = time.strftime("%Y%m%d")
            if code == 'SWIFT BIC':
                continue
            # elif conn._sismember_('already_get_info_queue', code) == 1:
            #     continue
            else:
                _my_log_.info('starting get banker info for:\t' + code)
                path = './html/' + str(date_now) + '/'
                if not os.path.exists(path):
                    os.mkdir(path)
                # conn._add_('already_get_info_queue', code)
                download._search_for_(code, 1)
                time.sleep(2)
        download._logout_banker()
    except Exception as e:
        _my_log_.error(e)
        download._logout_banker()

if __name__ == '__main__':
    '''
    the entrance of procedure
    '''
    _my_log_ = MyLog()
    # conn = database.RedisOperate()
    reload(sys)
    sys.setdefaultencoding('utf-8')
    start_spider()

    # url = test.TetsFunc().test('../_application/styles/core.css')
    # print(url)
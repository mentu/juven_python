#!/usr/bin/env python
# -*- coding: utf_8 -*-


# import MySQLdb
from configs import base_config
from bs4 import BeautifulSoup
from configs.mylog import MyLog
import bs4
import downloader
import os
import time


class Parser(object):
    def __init__(self):
        self.log = MyLog()
        # self.process = dict(base_config._full_details_)
        # self.conn = MySQLdb.connect(
        #     host=base_config._database_ip_
        #     , user=base_config._database_user_
        #     , passwd=base_config._database_pwd_
        #     , db=base_config._database_name_
        #     , charset="utf8")
        # self._test_database_()

    def _test_database_(self):
        '''
        test mysql database
        :return:
        '''
        cursor = self.conn.cursor()
        cursor.execute('select * from yhj_copyright_details')
        print(cursor.fetchall())
        cursor.close()

    def _parser_html_(self, content, filename):
        try:
            if not os._exists(filename):
                with open(filename, 'w+') as fp:
                    fp.write(content.encode('utf-8'))
                    fp.close()
        except Exception as e:
            self.log.error(e)
            downloader.Downloader()._logout_banker()

    def _get_result_(self, soup, point):
        try:
            self.log.info('get result')
            tables = soup.find_all('table')
            for table in tables:
                if isinstance(table, bs4.element.Tag):
                    for tr in table.find_all('tr'):
                        string = ''
                        if isinstance(tr, bs4.element.Tag):
                            for td in tr.find_all('td'):
                                if isinstance(td, bs4.element.Tag):
                                    string = string + ':\t' + td.text
                        print(string)
        except Exception as e:
            self.log.error(e)
            downloader.Downloader()._logout_banker()

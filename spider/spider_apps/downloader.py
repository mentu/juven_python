#!/usr/bin/env python
# -*- coding: utf_8 -*-


from configs.mylog import MyLog
import mechanize
import cookielib
import re
from configs import base_config
import time
from bs4 import BeautifulSoup
import parser
from datetime import datetime
import os
import platform
import database
import bs4
import urllib


class Downloader(object):
    '''
    html download and deal
    '''
    def __init__(self):
        '''
        init function of the class
        '''
        # self.redis = database.RedisOperate()
        # self._parser_util_ = parser.Parser()
        # init log file
        self.mylog = MyLog()
        # init the simulator of browser
        cj = cookielib.LWPCookieJar()
        self.br = mechanize.Browser()
        self.br.set_cookiejar(cj)
        self.br.set_handle_equiv(True)
        self.br.set_handle_redirect(True)
        self.br.set_handle_referer(True)
        self.br.set_handle_robots(False)
        self.br.set_handle_gzip(True)
        self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        self.br.addheaders = [
            ('user-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
        ]
        self._login_banker_(
            base_config.login_url,
            base_config.login_username,
            base_config.login_password)

    def _login_banker_(self, url, username, password):
        '''
        login to Bankersalmanac.com when the procedure start
        :return: 
        '''
        # open html by the url
        self.br.open(url)
        self.br.title()
        # select form from the html
        self.br.select_form(nr=1)
        # fill the username and password, and submit
        self.br.form['Username'] = username
        self.br.form['Password'] = password
        self.br.submit()
        login_resp_content = self.br.response().read()
        self.mylog.info("title:\t" + self.br.title())
        # judge the result of login
        if len(re.findall('already logged in', login_resp_content)) > 0:
            self.mylog.info('already login:\t' + username)
            time.sleep(60)
            self._login_banker_(
                base_config.login_url,
                base_config.login_username,
                base_config.login_password)
        elif len(re.findall('Invalid Username Or Password', login_resp_content)) > 0:
            self.mylog.info('username or password error:\t' + username + "\t" + password)
            self._login_banker_()
        elif 'Bankersalmanac.com - Institution Search' == self.br.title():
            self.mylog.info('login success')
        elif 'Bankersalmanac.com - Log-in to Bankersalmanac.com' == self.br.title():
            self.mylog.info('another condition happened')
            time.sleep(60)
            self._login_banker_(
                base_config.login_url,
                base_config.login_username,
                base_config.login_password)

    def _logout_banker(self):
        '''
        logout from Bankersalmanac.com when the procedure is over or happened something unknown
        :return: 
        '''
        self.mylog.info('starting logout')
        # judge the result exist log-out link or not
        try:
            # if not isinstance(self.br.response(), None):
            if len(re.findall('Log-out', self.br.response().read())) > 0:
                self.mylog.info('login success, and logout the website now')
                self.br.open(self.br.click_link(text='Log-out'))
            elif len(re.findall('400', self.br.response().read())) > 0:
                self.mylog.info('the html is error')
                self.br.back()
                self._logout_banker()
            elif self.br.title() == 'Bankersalmanac.com - Institution not found':
                self.mylog.info('not found the result html')
                self.br.back()
                self._logout_banker()
            elif self.br.title() == 'Bankersalmanac.com - Incorrect Access Permission':
                self.mylog.info('incorrect access permission')
                self.br.back()
                self._logout_banker()
            else:
                self.mylog.info('login failed and try to logout the website')
                self.br.open("https://accuity.com/?logout=true")
                # waiting for 5 minutes
                self.mylog.info('waiting for 5 minutes, and retry again')
                time.sleep(300)
                self._login_banker_(
                    base_config.login_url,
                    base_config.login_username,
                    base_config.login_password)
        except Exception as e:
            self.mylog.error(e)

    def _search_for_(self, swift_code, num):
        '''
        search for by swift code
        :param swift_code: swift
        :param swift_code: count
        :return: 
        '''
        try:
            # open the html of search by url
            self.br.open(base_config._search_detail_url_)
            if not self.br.title() == 'Bankersalmanac.com - Log-in to Bankersalmanac.com':
                # select form from the html
                self.br.select_form(nr=0)
                self.br.form['SearchText'] = swift_code
                self.br.submit()
                # judge the result of details
                print(self.br.title())
                if len(re.findall('Institution Search results for SWIFT/BIC', self.br.title())) > 0:
                    self.mylog.info('get details html success by swift code:\t' + swift_code)
                    date_now = time.strftime("%Y%m%d")
                    # get all details urls
                    soup = BeautifulSoup(self.br.response().read(), 'html.parser', from_encoding='utf-8')
                    for _url_details_ in soup.find_all('a', attrs={'tabindex':'1'}):
                        url = str(_url_details_.get('href')).encode("utf-8").strip().replace("\r\n", "").replace('\t', '')
                        # open the details page
                        self.br.open(base_config.details_url + url)
                        swift = str(url).split('&')[-1].split('#')[0].split('=')[1].replace('+', '')
                        filename = './html/' + str(date_now) + '/' + swift + '.html'
                        if not os._exists(filename):
                            print(filename)
                            with open(filename, 'w+') as fp:
                                fp.write(self.br.response().read().encode('utf-8'))
                                fp.close()
                                time.sleep(1)
                                self._get_files_()
                        else:
                            self.mylog.info('file already exist')
                else:
                    num = int(num) + 1
                    if num > 3:
                        self.mylog.error('query failed by:\t' + swift_code)
                        # self.redis._add_('error_queue', swift_code)
                    else:
                        self._search_for_(swift_code, num)
            else:
                self.mylog.info('not login Bankersalmanac.com')
                self._login_banker_(
                    base_config.login_url,
                    base_config.login_username,
                    base_config.login_password)
        except Exception as e:
            # self.redis._add_('error_queue', swift_code)
            self.mylog.error(e)
            self._logout_banker()

    def _get_files_(self):
        '''
        get js, css and picture file from the details html
        :param content:
        :return:
        '''
        try:
            date_now = time.strftime("%Y%m%d")
            soup = BeautifulSoup(self.br.response().read(), 'html.parser', from_encoding='utf-8')

            # get css file from the details html
            csss = soup.find_all('link', href=re.compile('\.css'))
            _root_url_ = base_config.root_url
            for css in csss:
                if isinstance(css, bs4.element.Tag):
                    url = ''
                    path = './html/'
                    for con in str(css.get('href')).split('/'):
                        if con == "..":
                            continue
                        elif len(re.findall('\.css', con)) > 0:
                            file_path = path + con
                            url = _root_url_ + url + con
                            if not os._exists(file_path):
                                print('url:\t' + url)
                                print('file_path:\t' + file_path)
                                self.br.open(url)
                                with open(file_path, 'w+') as fp:
                                    fp.write(self.br.response().read())
                                    fp.close()
                                    time.sleep(0.1)
                                self.br.back()
                        else:
                            path = path + con + '/'
                            if not os.path.exists(path):
                                os.mkdir(path)
                            url = url + con + '/'

            # get picture from the details html
            pic_urls = soup.find_all('img', src=re.compile('\.(gif|png|jpg)'))
            for pic in pic_urls:
                if isinstance(pic, bs4.element.Tag):
                    pic_url = ''
                    if str(pic.get('src')).startswith('/'):
                        pic_path = '/'
                    elif str(pic.get('src')).startswith('[a-zA-Z]'):
                        pic_path = './html/' + str(date_now) + '/'
                    for pt in str(pic.get('src')).split('/'):
                        if pt == '..' or pt == '':
                            continue
                        elif len(re.findall('\.(gif|png|jpg)', pt)) > 0:
                            pic_path = pic_path + pt
                            pic_url = _root_url_ + pic_url + pt
                            if not os.path.exists(pic_path):
                                print('pic_url:\t' + pic_url)
                                print('pic_path:\t' + pic_path)
                                urllib.urlretrieve(pic_url, pic_path)
                                time.sleep(0.1)
                        else:
                            pic_path = pic_path + pt + '/'
                            if not os.path.exists(pic_path):
                                os.mkdir(pic_path)
                            pic_url = pic_url + pt + '/'
        except Exception as e:
            self.mylog.error(e)
            self.br.back()

    def _get_detail_(self, code):
        '''
        get full details of banker
        :return:
        '''
        try:
            # judge the html is the full details or not
            print(self.br.title())
            if self.br.title() == 'Bankersalmanac.com - Incorrect Access Permission':
                self.mylog.info('current page is not full details html, searching by the swift code again')
                # self._search_for_(code)
            elif self.br.title() == 'Bankersalmanac.com - Institution not found':
                self.mylog.info('can not found the details html, searching by the swift code again')
                # self._search_for_(code, 2)
            else:
                links = []
                for link in self.br.links(url_regex='fid'):
                    links.append(link.text)
                if 'Full Details' in links:
                    self.mylog.info('there is details link in this html')
                    self.br.open(self.br.click_link(text='Full Details'))
                    print(self.br.title())
                    self._parser_util_._parser_html_(self.br.response().read(), 'head_office_details')
                    self._full_details_html()
                else:
                    self.mylog.info('there is not details link in this html')
        except Exception as e:
            self.mylog.error(e)
            self._logout_banker()

    def _full_details_html(self):
        try:
            if len(re.findall('Full Details', self.br.title())) > 0:
                self.mylog.info('get the details html success, starting parser the result from head office details')
                # self._parser_util_._parser_html_(self.br.response().read(), 'head_office_details')
            else:
                self.mylog.info('current html is not the details page, get details html first')
                self.br.open(self.br.click_link(text='Full Details'))
                self._full_details_html()
        except Exception as e:
            self.mylog.error(e)
            self._logout_banker()
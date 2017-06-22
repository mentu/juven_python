# coding:utf-8
__author__ = 'chenhuachao'
# --------------------------------
# Created by chenhuachao  on 201x/xx/xx.
# ---------------------------------

#添加计划任务，对出错的爬虫url进行补充重试爬取

#0  1 * * * root /usr/local/bin/python3 -m credit_spider.spider_app.spider_main

import os
def start_error_spider_relay():
    '''每天凌晨执行错误重试脚本。

    :return:
    '''
    os.popen('python3 -m spider_app.spider_error_relay&')

if __name__ == '__main__':
    start_error_spider_relay()



#!/usr/bin/env python
# -*- coding: utf_8 -*-

import getpass
from datetime import datetime, timedelta
import logging
import os

class MyLog(object):
    '''
        日志模块
    '''
    def __init__(self):  # 构造函数
        user = getpass.getuser()
        self.logger = logging.getLogger(user)
        self.logger.setLevel(logging.DEBUG)
        if not os.path.exists('./logs/'):
            os.mkdir('./logs/')

        #保留三天日志
        #old_file = './logs/' + str(datetime.now().replace(day=datetime.now().day - 3).date()) + '.log'
        #if os.path.exists(old_file):
        #    os.remove(old_file)
        log_file = './logs/' + str(datetime.now().date()) + '.log'
        formatter = logging.Formatter('%(asctime)-12s %(levelname)-8s %(name)-10s %(message)-12s')

        log_hand = logging.FileHandler(log_file)
        log_hand.setFormatter(formatter)
        log_hand.setLevel(logging.ERROR)

        log_hand_st = logging.StreamHandler()
        log_hand_st.setFormatter(formatter)

        self.logger.addHandler(log_hand)
        self.logger.addHandler(log_hand_st)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)

if __name__ == '__main__':
    log = MyLog()
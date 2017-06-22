#!C:\Python27\python.exe
# coding: utf-8

__author__ = 'yueyt'

import datetime
from queue import Queue

from config_tt import base_config
from config_tt.log_config import logger
from spider_app.celery_main import app
from spider_app.spider_main import SpiderByQueue


@app.task
def spider_tasks(org_code):
    # queue
    url_or_data_queue = Queue()

    # 放入初始url
    #url_or_data_queue.put([base_config.start_point, '', dict(sdeporgcode=org_code)])
    url_or_data_queue.put([base_config.start_point, '', dict(loancardno=org_code)])

    spider = SpiderByQueue(url_or_data_queue)
    start_time = datetime.datetime.now()
    logger.info('{} start loancardno:{} ...'.format('-' * 80, org_code))
    spider.run()
    logger.info('{} end loancardno:{}, token time:{} ...'.format(
        '-' * 80, org_code, datetime.datetime.now() - start_time))

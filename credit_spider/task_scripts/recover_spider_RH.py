# coding:utf-8
__author__ = 'chenhuachao'
# --------------------------------
# Created by chenhuachao  on 201x/xx/xx.
# ---------------------------------
#恢复人行征信的爬虫程序脚本0  8 * * * root /usr/local/bin/python3 /home/crontab_task/recover_spider_RH.py
# redis_config = {
#     'host':'182.119.136.141',
#     'port':6379,
#     'db':0,
# }
import redis
import datetime
weekday = datetime.datetime.now().weekday()
from config_tt import base_config
conn = redis.StrictRedis(**base_config.redis_config)
# if weekday not in [5,6]:
conn.hset('rh_search_date_range','delay_time',0.5)

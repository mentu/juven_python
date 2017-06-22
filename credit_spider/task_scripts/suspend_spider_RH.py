# coding:utf-8
__author__ = 'chenhuachao'
# --------------------------------
# Created by chenhuachao  on 201x/xx/xx.
# ---------------------------------
#暂停人行征信的爬虫程序  30  21 * * * root /usr/local/bin/python3 /home/crontab_task/suspend_spider_RH.py
# redis_config = {
#     'host':'182.119.136.141',
#     'port':6379,
#     'db':0,
# }
import datetime
import redis
from config_tt import base_config
weekday = datetime.datetime.now().weekday()
conn = redis.StrictRedis(**base_config.redis_config)
# if weekday == 4:
#     conn.hset('rh_search_date_range','delay_time',208800)
# elif weekday in [0,1,2,3]:
conn.hset('rh_search_date_range','delay_time',3600)

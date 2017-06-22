# coding:utf-8
__author__ = 'chenhuachao'
# --------------------------------
# Created by chenhuachao  on 201x/xx/xx.
# ---------------------------------
#只能在项目初始化的时候运行一次，创建基础环境需要的key
import redis
from config_tt import base_config
conn = redis.StrictRedis(**base_config.redis_config)
def assign_task():
    '''初始化爬虫需要爬取的固定档期。
    '''
    #清空环境 rh_spider_task_period档期汇总表；rh_spider_done_orgcode正在爬取的组织机构代码
    for date in ['2014-03-31','2014-06-30','2014-09-30','2014-12-31',
                 '2015-03-31','2015-06-30','2015-09-30','2015-12-31',
                 '2016-03-31','2016-06-30','2016-09-30','2016-12-31']:
        conn.delete(date,'rh_spider_task_period','rh_spider_done_orgcode')
    #写入待爬档期
    for date in ['2014-03-31','2014-06-30','2014-09-30','2014-12-31',
                 '2015-03-31','2015-06-30','2015-09-30','2015-12-31',
                 '2016-03-31','2016-06-30','2016-09-30','2016-12-31']:
        #写入档期汇总集合
        conn.sadd('rh_spider_task_period',date)
        #创建单档期文档，用于存储爬取完成的企业组织机构代码
        conn.sadd(date,'')
    conn.hset('rh_search_date_range','delay_time','0.2')
    print('初始化完成')

if __name__ == '__main__':
    assign_task()
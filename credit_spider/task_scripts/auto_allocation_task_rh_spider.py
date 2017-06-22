# coding:utf-8
__author__ = 'chenhuachao'
# --------------------------------
# Created by chenhuachao  on 201x/xx/xx.
# ---------------------------------
import datetime
from config_tt import base_config
# redis_config = {
#     'host':'182.119.136.141',
#     'port':6379,
#     'db':0,
# }
import redis
conn = redis.StrictRedis(**base_config.redis_config)
class AutoAllocationTask_RhSpider(object):
    def task_date_com(self):
        """人行征信的爬虫分发任务的函数，提取适当的任务周期
        按照计划任务部署，每天凌晨0点执行    0 0 * * *
        """
        today = datetime.date.today().strftime("%Y-%m-%d")
        # today = '2016-01-10'
        cut_date = ''.join(today.split('-'))[-4:]
        year = today[:4]
        print(cut_date)
        print(today[:4])
        if cut_date == '0410':
            last_quarter_start, last_quarter_end = year+'-01-01',year+'-03-31'
        elif cut_date == '0710':
            last_quarter_start, last_quarter_end = year+'-04-01',year+'-06-30'
        elif cut_date == "1010":
            last_quarter_start, last_quarter_end = year+'-07-01',year+'-09-30'
        elif cut_date == "0110":
            last_quarter_start, last_quarter_end = str(int(year)-1)+'-10-01',str(int(year)-1)+'-12-31'
        else:
            last_quarter_start, last_quarter_end='',''
        return last_quarter_start, last_quarter_end
    def allocation_task(self):
        """对任务日期进行检测，如果通过，则分配任务到redis中，key为set集合类型

        :return:
        """
        last_quarter_start, last_quarter_end = self.task_date_com()
        if last_quarter_start and last_quarter_end:
            result = conn.sadd('rh_spider_task_period',last_quarter_end)
            task_result = conn.sadd(last_quarter_end,'')
            print(result,task_result)
        print(last_quarter_start,last_quarter_end)
if __name__ == '__main__':
    starttask = AutoAllocationTask_RhSpider()
    starttask.allocation_task()

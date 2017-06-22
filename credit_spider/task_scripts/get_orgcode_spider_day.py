# coding:utf-8
__author__ = 'chenhuachao'
# --------------------------------
# Created by chenhuachao  on 201x/xx/xx.
# 每天导出需要爬取的企业机构号码 ，跟已经爬取过的企业机构号码求差集，然后放入待爬的redis队列中
# ---------------------------------
import time
import ibm_db
import redis
from config_tt import base_config
import traceback
# hostname = '182.217.16.45'
# port = 60000
# user = 'db2iiass'
# password = 'db2iiass'
# database = 'DBIASS'
# tabschema = 'RHTEST'
# tabschema = 'DB2IIASS'
# redis_config = {
#     'host':'182.119.136.140',
#     'port':6379,
#     'db':0,
#     'password':'123456'
# }
class HtmlOutputer(object):
    def __init__(self):
            conn_str = "DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (
                base_config.database,base_config.hostname,base_config.port,base_config.user,base_config.password)
            self.conn = ibm_db.connect(conn_str, '', '')
            self.redis_conn = redis.StrictRedis(**base_config.redis_config)
    def get_table_data_day(self):
        '''每天获取待爬清单'''
        all_spider_list = []
        # spider_done = self.get_spider_done()
        # 清空redis队列
        self.redis_conn.delete('high_level_spider_orgcode_queue','low_level_spider_orgcode_queue')
        #获取爬取档期
        # searchdate = self.redis_conn.hget('rh_search_date_range','last_quarter_end')
        # searchdate = searchdate.decode()
        #查询需要爬取的企业机构号
        # query_tables_sql = "select distinct CUST_NAME,ORG_CODE,CUST_ID from {0}.PRIORITY_CLIENT_LIST  where FLAG=1 and ORG_CODE !='null'".format(
        #   base_config.tabschema.upper() or base_config.user.upper())
        #query_tables_sql = "select CUST_CODE from {0}.RISK_MNIT_QUERY_RH_LIST".format(base_config.tabschema.upper() or base_config.user.upper())
        query_tables_sql = "select MID_SIGN_CODE from {0}.RISK_MNIT_QUERY_RH_LIST".format(base_config.tabschema.upper() or base_config.user.upper())
        result_query = ibm_db.exec_immediate(self.conn, query_tables_sql)
        row = ibm_db.fetch_assoc(result_query)
        while (row):
            all_spider_list.append(row.get("MID_SIGN_CODE"))
            row = ibm_db.fetch_assoc(result_query)
        #每天筛选出未爬取的清单
        # wait_spider_list = list(set(al_spider_list).difference(set(spider_done)))
        # 重新插入每天筛选的待爬清单
        print(all_spider_list)
        self.redis_conn.delete('high_level_spider_orgcode_queue')

        #将中征码保存到REDIS待爬队列中：high_level_spider_orgcode_queue
        for orgcode in all_spider_list:
            if orgcode:
                print(orgcode)
                self.redis_conn.lpush('high_level_spider_orgcode_queue',orgcode)
        ibm_db.close(self.conn)
    # def get_spider_done(self):
    #     '''
    #     获取已经爬完的企业机构代码并返回
    #     '''
    #     spider_done = []
    #     query_sql = 'select ORG_CODE from {0}.RH_CUST_QUEUE;'.format(tabschema.upper())
    #     result_query = ibm_db.exec_immediate(self.conn, query_sql)
    #     row = ibm_db.fetch_assoc(result_query)
    #     while (row):
    #         print(row)
    #         spider_done.append(row.get('ORG_CODE'))
    #         row = ibm_db.fetch_assoc(result_query)
    #     return spider_done



if __name__ == '__main__':
    HtmlOutputer().get_table_data_day()
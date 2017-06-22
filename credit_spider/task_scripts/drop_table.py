# coding:utf-8
__author__ = 'chenhuachao'
# --------------------------------
# Created by chenhuachao  on 201x/xx/xx.
#清空征信表的脚本文件
# ---------------------------------
import time
import pymysql
import ibm_db
import traceback
hostname = '182.217.16.45'
port = 60000
user = 'db2iiass'
password = 'db2iiass'
database = 'DBIASS'
# tabschema = 'RHTEST'
tabschema = 'RH'
class HtmlOutputer(object):
    def __init__(self):
            conn_str = "DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (
                database,hostname,port,user,password)
            self.conn = ibm_db.connect(conn_str, '', '')

    def delete_all_table_data(self):
        query_tables_sql = "select trim(tabschema) as tabschema, tabname FROM syscat.tables WHERE tabschema = '{}'".format(
          tabschema.upper() or user.upper())
        result_query = ibm_db.exec_immediate(self.conn, query_tables_sql)
        row = ibm_db.fetch_assoc(result_query)
        while (row):
            if row.get('TABNAME').startswith("RH_") and row.get('TABNAME') not in  ['RH_CUST_QUEUE','RH_ERROR_SPIDER','RH_SPIDER_QUEUE_LIST']:
                # delete_sql = "truncate table {TABSCHEMA}.{TABNAME} immediate;".format(**row)
                # print(delete_sql)
                sql_delete = "delete from {TABSCHEMA}.{TABNAME} where  ='1101000002264820'".format(**row)
                print(sql_delete)
                # delete_sql2 = "delete from {TABSCHEMA}.{TABNAME} where MIDSIGNCODE='3309060000195576' and date(uploadtime)='2016-12-15';".format(**row)
                # print(delete_sql2)
                try:
                    # ibm_db.exec_immediate(self.conn, sql_delete)
                    ibm_db.exec_immediate(self.conn, sql_delete)
                    # ibm_db.exec_immediate(self.conn, delete_sql2)
                except Exception as e:
                    print('error state code:{}'.format(ibm_db.stmt_error()),"error state=",e)
                # time.sleep(0.1)
            row = ibm_db.fetch_assoc(result_query)
            ibm_db.commit(self.conn)
    def close(self):
        ibm_db.close(self.conn)

if __name__ == '__main__':
    HtmlOutputer().delete_all_table_data()
    HtmlOutputer().close()
'''
2016-12-15爬取重复数据
select * from DB2IIASS.rh_bdbguaranteesum where MIDSIGNCODE='3205830002477022';  1
select * from DB2IIASS.rh_bdbguaranteesum where MIDSIGNCODE='3309060000195576';  1
'''
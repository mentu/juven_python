#!/usr/bin/env python
# coding: utf8
__author__ = 'yueyt'

import pymysql
import ibm_db
import time
import os
import hashlib
from config_tt import base_config
from config_tt.log_config import logger



def filter_organization_code(code, startdate):
    '''
    贷款银行合同号解析func
    :param code:
    :return:
    '''
    organization_name = ''
    if code.startswith('HET'):
        organization_name = '建设银行'
    elif code.startswith('CIIT'):
        organization_name = '兴业信托'
    elif len(code) == 9:
        if code[0:2] == startdate[2:4]:
            organization_name = '广东发展银行'
    elif len(code) == 10:
        organization_name = '招商银行'
    elif len(code) == 13:
        organization_name = '中信银行'
    elif code.startswith('BC'):
        organization_name = '上海浦发银行'
    elif len(code) == 11:
        organization_name = '中国银行'
    elif len(code) == 19:
        organization_name = '国开行'
    elif '进出口' in code:
        organization_name = '中国进出口银行'
    elif code.startswith('xd'):
        organization_name = '兴业银行'
    elif len(code) == 17 and not code.startswith('CIIT'):
        try:
            if code[6:10] == startdate[0:4]:
                organization_name = '农业银行'
        except:
            pass
    elif len(code) == 14:
        try:
            if code[4:8] == startdate[0:4]:  # 5-8
                organization_name = '民生银行'
            elif code[2:6] == startdate[0:4]:  # 3-6
                organization_name = '光大银行'
        except:
            pass
    elif len(code.split('_')[0]) == 15 and len(code.split('_')) >= 2:
        organization_name = '工商银行'
    elif len(code) > 10:
        if code[10] == 'M' or code[10] == 'A':
            organization_name = '交通银行'
    if not organization_name:
        organization_name = '其它机构'
    return organization_name


def draft_filter(code):
    '''
    银票兑换解析函数
    :return:
    '''
    yinpiao_code = {
        "001": "中国人民银行",
        "102": "中国工商银行",
        "103": "中国农业银行",
        "104": "中国银行",
        "105": "中国建设银行",
        "201": "国家开发银行",
        "202": "中国进出口银行",
        "203": "农业发展银行",
        "301": "交通银行",
        "302": "中信银行",
        "303": "中国光大银行",
        "304": "华夏银行",
        "305": "中国民生银行",
        "306": "广东发展银行",
        "307": "平安银行",
        "308": "招商银行",
        "309": "兴业银行",
        "310": "上海浦东发展银行",
        "315": "恒丰银行",
        "316": "浙商银行",
        "318": "渤海银行",
    }
    if len(code) == 16:
        code_start = code[0:3]
        if yinpiao_code.get(code_start):
            organization_name = yinpiao_code.get(code_start)
        else:
            organization_name = '其它机构'
    else:
        organization_name = '其它机构'
    return organization_name


class HtmlOutputer(object):
    def __init__(self):
        if base_config.database_type == 'mysql':
            self.conn = pymysql.connect(host=base_config.hostname, port=base_config.port,
                                        user=base_config.user, passwd=base_config.password,
                                        db=base_config.database,
                                        charset=base_config.codeset, use_unicode=True)
            self.cursor = self.conn.cursor()
        else:
            print(base_config.database, base_config.hostname, base_config.port, base_config.user, base_config.password)
            conn_str = "DATABASE=%s;HOSTNAME=%s;PORT=%d;PROTOCOL=TCPIP;UID=%s;PWD=%s;" % (
                base_config.database, base_config.hostname, base_config.port, base_config.user, base_config.password)
            self.conn = ibm_db.connect(conn_str, '', '')

    def save_dict_into_mysql(self, processor_type, data):
        if not isinstance(data, dict):
            return
        table = data.pop('table')
        placeholders = ','.join(['%s'] * len(data))
        columns = ','.join(data.keys())
        sql = "INSERT INTO {}({}) VALUES({})".format(table, columns, placeholders)
        # debug
        logger.info('processor_type:[{}], sql:[{} {}]'.format(processor_type, sql, tuple(data.values())))
        try:
            self.cursor.execute(sql, tuple(data.values()))
        except pymysql.Error as e:
            logger.error('Oops, i got the fault: {}, {} {}'.format(e, sql, tuple(data.values())))
        self.conn.commit()

    def save_dict_into_ibmdb(self, processor_type, data):
        if not isinstance(data, dict):
            return
        table = data.pop('table')
        # 贷款银行合同号解析
        if table in base_config.table_dict.keys():
            if data.get(base_config.table_dict.get(table).get('contractcode')) and data.get(
                    base_config.table_dict.get(table).get('orgname')) == '******':
                data[base_config.table_dict.get(table).get('orgname')] = filter_organization_code(
                    data.get(base_config.table_dict.get(table).get('contractcode')),
                    data.get(base_config.table_dict.get(table).get('date')))
        # 银票号解析
        elif table in base_config.draft_dict.keys():
            if data.get(base_config.draft_dict.get(table).get('contractcode')) and data.get(
                    base_config.draft_dict.get(table).get('orgname')) == '******':
                data[base_config.draft_dict.get(table).get('orgname')] = draft_filter(
                    data.get(base_config.draft_dict.get(table).get('contractcode')))
        placeholders = ','.join(['?'] * len(data))
        columns = ','.join(data.keys())
        statement = "INSERT INTO {}.{}({}) VALUES({})".format(base_config.tabschema, table, columns,
                                                              placeholders)
        # debug
        logger.info('processor_type:[{}], sql:[{} {}]'.format(processor_type, statement, tuple(data.values())))
        try:
            stmt = ibm_db.prepare(self.conn, statement)
            ibm_db.execute(stmt, tuple(data.values()))
        except:
            print('error state code:{}'.format(ibm_db.stmt_error()))

    def save_records(self, processor_type, data):
        if isinstance(data, list):
            for subdata in data:
                if base_config.database_type == 'mysql':
                    self.save_dict_into_mysql(processor_type, subdata)
                else:
                    self.save_dict_into_ibmdb(processor_type, subdata)
        elif isinstance(data, dict):
            if base_config.database_type == 'mysql':
                self.save_dict_into_mysql(processor_type, data)
            else:
                self.save_dict_into_ibmdb(processor_type, data)

        if base_config.database_type == 'mysql':
            self.conn.commit()
        else:
            ibm_db.commit(self.conn)
    def insert_data(self,sql):
        try:
            print(sql)
            ibm_db.exec_immediate(self.conn,sql)
        except:
            import traceback
            traceback.print_exc()
            pass
        else:
            ibm_db.commit(self.conn)
    def update_spider_done(self,orgcode):
        '''爬取完成的企业进行入库记录'''
        try:
            #1.更新待爬清单的状态为爬取完成
            update_spider_queue_table_sql = "update {0}.RH_SPIDER_QUEUE_LIST set STATUS='2' where ORGCODE='{1}' and SEARCHDATE='{2}';".format(
                base_config.tabschema.upper(),orgcode,os.getenv('last_quarter_end')
            )
            ibm_db.exec_immediate(self.conn,update_spider_queue_table_sql)
            ibm_db.commit(self.conn)
            #2.更新爬取完成清单的内容，如果没有出错，就插入爬取完成表。出错就不插入
            error_spider_record_sql = "select ORGCODE from {0}.RH_ERROR_SPIDER where SEARCHDATE='{1}' and ORGCODE='{2}' and date(UPLOADTIME)='{3}';".format(
                base_config.tabschema.upper(),os.getenv('last_quarter_end'),orgcode,time.strftime('%Y-%m-%d',time.localtime(time.time()))
            )
            error_spider_record = ibm_db.exec_immediate(self.conn,error_spider_record_sql)
            row = ibm_db.fetch_assoc(error_spider_record)
            # if row:
            #     pass
            # if not row:

            # 成功与否，都添加记录到RH_CUST_QUEUE中
            #select CUSTNAME,CUSTID from DB2IIASS.DESK_SXGL0431_D where ORGCERTCODE='93125730-6';
            sql = "select distinct CUSTNAME,CUSTID from  {0}.DESK_SXGL0431_D where LNCARDNO='{1}';".format(base_config.hongduntabschema.upper(),orgcode)
            result_query = ibm_db.exec_immediate(self.conn,sql)
            row = ibm_db.fetch_assoc(result_query)
            while (row):
                # print(row)
                insert_sql = "insert into {0}.RH_CUST_QUEUE(ENT_NAME,CUS_NO,ORG_CODE,MIDSIGNCODE,SEARCHDATE,FINISH_DATE) values ('{1}','{2}','{3}','{4}','{5}','{6}')".format(
                    base_config.tabschema,row.get('CUSTNAME'),row.get('CUSTID'),orgcode,os.getenv('midsigncode'),os.getenv('last_quarter_end'),
                    time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))

                ibm_db.exec_immediate(self.conn,insert_sql)
                ibm_db.commit(self.conn)
                row = ibm_db.fetch_assoc(result_query)
                #os.environ['credit_status'] = '0'
                #HtmlOutputer().write_log_with_zhengxin()
        except Exception as e:
            logger.error("爬取完成的企业进行入库记录error",e)
            pass
    def select_spier_date(self):
        '''判断当天是不是工作日
        :return:
        '''
        date = time.strftime("%Y%m%d",time.localtime(time.time()))
        year,month,day =date[:4],date[4:6],date[6:]
        select_sql = "select HOLIDAY_BUSI_FLAG from {0}.CB_HOLIDAY_MAINTEN  where YEAR='{1}' and  MONTH='{2}' and AREA_CODE='156'".format(
                        base_config.tabschema,year,month)
        result = ibm_db.exec_immediate(self.conn,select_sql)
        row = ibm_db.fetch_assoc(result)
        return row.get('HOLIDAY_BUSI_FLAG')[int(day)-1] if row else ''
    def write_log_with_zhengxin(self):
        '''
        记录登陆人行征信查询页面的次数及日志。用于以后的记录查询
        :return:
        '''
        try:
            orgcode = os.getenv('orgcode')
            # 获取所要查询机构代码的查询用户
            # USER_CODE = ibm_db.exec_immediate(self.conn,"select USER_CODE,CUST_NAME,CLIENT_TYPE from RH.PRIORITY_CLIENT_LIST where ORG_CODE='{0}'".format(orgcode))
            # usercode = ibm_db.fetcha_assoc(USER_CODE)
            # 获取查询用户的机构和部门
            # ENT_NAME 企业名称
            # USER_NAME 用户名称
            # USER_CODE 用户CODE
            # USER_ORG_NAME 用户归属机构名称
            # USER_BRANCH_NAME 用户所属分行名称

            # 判断改客户是否已经爬取过
            query = "select distinct ORG_CODE,MIDSIGNCODE,CUS_NO from {0}.RH_CUST_QUEUE where MIDSIGNCODE='{1}';".format(
                base_config.tabschema, orgcode)
            org_Info = ibm_db.exec_immediate(self.conn, query)
            row = ibm_db.fetch_assoc(org_Info)
            if row:
                status = '0'
            if not row:
                status = '1'
            # 添加登陆信息到记录表中
            sql = "select ENT_NAME,USER_NAME,USER_CODE,USER_ORG_NAME,USER_BRANCH_NAME,QUERY_REASON from RH.RISK_MNIT_QUERY_RH_LIST where MID_SIGN_CODE='{0}'".format(
                orgcode)
            result = ibm_db.exec_immediate(self.conn, sql)
            orgdetail = ibm_db.fetch_assoc(result)
            if not isinstance(orgdetail,bool):
                current_data = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
                insertsql = "insert into RH.RH_LOGIN_ZHENGXIN_WEB_LOG" \
                            " (USER_CODE,CUST_NAME,ORGCODE,USERID,PASSWORD,STATUS,UPLOADTIME,CLIENT_TYPE,ORG_NAME,SEARCH_TYPE,USER_NAME,USER_BRANCH_NAME,CUST_CODE) " \
                            "values ('{0}','{1}','{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}','{11}','{12}')".format(
                    orgdetail.get('USER_CODE', ''),
                    orgdetail.get('ENT_NAME', ''), base_config.login_post_data.get('orgCode'),
                    base_config.login_post_data.get('userid'),
                    hashlib.md5(base_config.login_post_data.get('password').encode('utf8')).hexdigest(),
                    os.getenv('credit_status'), current_data, status,
                    orgdetail.get('USER_ORG_NAME', ''), orgdetail.get('QUERY_REASON', ''), orgdetail.get('USER_NAME', ''),
                    orgdetail.get('USER_BRANCH_NAME', ''), orgcode)
                # print(insertsql)
                ibm_db.exec_immediate(self.conn, insertsql)
                ibm_db.commit(self.conn)
            else:
                print("企业信息为空")
        except Exception as e:
            logger.error("添加登陆记录时出错error",e)

    def get_query_reason(self):
        '''
        查询原因选择
        :return:
        '''
        try:
            orgcode = os.getenv('orgcode')
            sql = "select QUERY_REASON from {0}.RISK_MNIT_QUERY_RH_LIST where MID_SIGN_CODE='{1}'".format(base_config.tabschema,orgcode)
            result = ibm_db.exec_immediate(self.conn, sql)
            orgdetail = ibm_db.fetch_assoc(result)
            if isinstance(orgdetail,bool):
                return ''
            else:
                if orgdetail.get('QUERY_REASON') == '贷前调查':
                    return '01'
                elif orgdetail.get('QUERY_REASON') == '贷中操作':
                    return '02'
                elif orgdetail.get('QUERY_REASON') == '贷后管理':
                    return '03'
                elif orgdetail.get('QUERY_REASON') == '关联查询':
                    return '04'
                else:
                    return ''
        except Exception as e:
            logger.error("查询原因获取失败error",e)
            return ''
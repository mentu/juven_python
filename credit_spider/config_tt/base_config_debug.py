#!/usr/bin/env python
# coding: utf-8
__author__ = 'yueyt'

import os

basedir = os.path.abspath(os.path.dirname(__file__))

# 爬取数据的存储位置
database_type = 'db2'
codeset = 'utf8'

### for mysql
# hostname = '182.119.166.119'
# port = 3306
# user = 'root'
# password = 'root'
# database = 'credit'

### for ibm db2测试
port = 60000
hostname = '182.217.16.45'
user = 'db2iiass' #测试库
password = 'db2iiass'
database = 'DBIASS' #测试库
tabschema = 'RH' #测试库
hongduntabschema = 'HD'
#测试
redis_config = {
    'host':'182.119.136.141',
    'port':6379,
    'db':0,
}
# 并发线程数
concurrent_thread_amount = 3
# 下载延迟秒数
download_delay_min = 1
download_delay_max = 2
# http request timeout
request_timeout = 60

# base root url
root_url = 'http://182.247.7.50:7001/shwebroot/'
# root_url = 'http://182.247.7.98:8001/webroottest/' #测试
page_encoding = 'gbk'
# 登录网站的首页
login_url = root_url + 'logon.do'
login_post_data = {
    'orgCode': '29003010005',
    'userid': 'JT-ZH-P3026',
    'password': 'Letsrock-risk'
}
# login_post_data = {
#     'orgCode': '29003010005',
#     'userid': 'JT-ZH-P015',
#     'password': '12345678zaq'
# }

# 下载器使用的request header
request_header = {
    'Host': '182.247.7.50:7001',
    'Connection': 'Keep-Alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Accept': 'image/jpeg, application/x-ms-application, image/gif, application/xaml+xml, image/pjpeg, application/x-ms-xbap, application/x-shockwave-flash, application/vnd.ms-powerpoint, application/msword, application/x-silverlight, application/vnd.ms-excel, */*',
    'Origin': 'http://182.247.7.50:7001',
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; Tablet PC 2.0; InfoPath.3)',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': root_url,
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN',
}

# 要搜索的企业机构号和start URL
start_point = 'orgcodeinfo'
# start_point = 'rh_fashenge_piaojutixian_list'
# search_org_codes = ['10000349-5', '55830728-X', '74731084-0', '78739972-0']
# '716575125','177685391','704737211','565001967'
search_org_codes = ['55305553-8']
# 贷款银行合同号解析-配置表
table_dict = {
    "rh_loaninfo": {'contractcode': 'contractnumber', 'orgname': 'financialinstitution', 'date': 'startdate'},
    "rh_loaninfo_f": {'contractcode': 'contractnumber', 'orgname': 'financialinstitution', 'date': 'startdate'},
    "rh_loaninfo_d": {'contractcode': 'contractnumber', 'orgname': 'financialinstitution', 'date': 'startdate'},
    "rh_specialloaninfo": {'contractcode': 'contractnumber', 'orgname': 'financialinstitution', 'date': 'startdate'},
    "rh_specialloaninfo_d": {'contractcode': 'contractnumber', 'orgname': 'financialinstitution', 'date': 'startdate'},
    "rh_specialloaninfo_f": {'contractcode': 'contractnumber', 'orgname': 'financialinstitution', 'date': 'startdate'},
    "rh_fagreementinfo_f": {'contractcode': 'financecode', 'orgname': 'institutionname', 'date': 'starttime'},
    "rh_fagreementinfo_d": {'contractcode': 'financecode', 'orgname': 'institutionname', 'date': 'starttime'},
    "rh_fagreementinfo": {'contractcode': 'financecode', 'orgname': 'institutionname', 'date': 'starttime'},
    "rh_factoringinfo": {'contractcode': 'factoringcode', 'orgname': 'institutionname', 'date': 'sydate'},
    "rh_factoringinfo_f": {'contractcode': 'factoringcode', 'orgname': 'institutionname', 'date': 'sydate'},
    "rh_factoringinfo_d": {'contractcode': 'factoringcode', 'orgname': 'institutionname', 'date': 'sydate'},
    "rh_guaranteeha": {'contractcode': 'guaranteecode', 'orgname': 'institutionname', 'date': 'starttime'},
    "rh_guaranteeha_d": {'contractcode': 'guaranteecode', 'orgname': 'institutionname', 'date': 'starttime'},
    "rh_guaranteeha_f": {'contractcode': 'guaranteecode', 'orgname': 'institutionname', 'date': 'guarantstarttime'},
    "rh_guaranteecontractinfo": {'contractcode': 'contractencoding', 'orgname': 'institutionname',
                                 'date': 'signingdate'},
    "rh_guaranteecontractinfo_f": {'contractcode': 'contractencoding', 'orgname': 'institutionname',
                                   'date': 'signingdate'},
    "rh_mortgagecontract": {'contractcode': 'mortcontractcode', 'orgname': 'institutionname',
                            'date': 'businesssigntime'},
    "rh_mortgagecontract_f": {'contractcode': 'mortcontractcode', 'orgname': 'institutionname',
                              'date': 'businesssigntime'},
    "rh_borrowerpledgeinfo": {'contractcode': 'pledgecode', 'orgname': 'businessinst', 'date': 'signingdate'},
    "rh_borrowerpledgeinfo_f": {'contractcode': 'pledgecode', 'orgname': 'businessinst', 'date': 'signingdate'},
    'rh_martpad': {'contractcode': 'padcode', 'orgname': 'institutionname', 'date': 'paddate'},
    'rh_dbmortinfo': {'contractcode': 'mortcode', 'orgname': 'institutionname', 'date': 'signdate'},
    'rh_dbguaranteecontract': {'contractcode': 'guaranteecode', 'orgname': 'institutionname', 'date': 'signdate'},
    'rh_creditbalance': {'contractcode': 'creditcode', 'orgname': 'institutionname', 'date': 'issuingdate'},
    'rh_creditagreement': {'contractcode': 'creditagreementnumber', 'orgname': 'institutionname',
                           'date': 'creditagreementfrom'},
    'rh_bdbpledgecontract': {'contractcode': 'contractcode', 'orgname': 'institutionname', 'date': 'signingdate'},
    'rh_bdbmortgagecontract': {'contractcode': 'contractcode', 'orgname': 'institutionname', 'date': 'signingdate'},
    'rh_bdbguaranteecontractinfo': {'contractcode': 'guaranteecode', 'orgname': 'institutionname', 'date': 'signdate'},
}
# 银票号解析-配置表
draft_dict = {
    'rh_draft': {'contractcode': 'draftcode', 'orgname': 'institutionname'},
    'rh_draft_f': {'contractcode': 'draftcode', 'orgname': 'institutionname'},
    'rh_draft_d': {'contractcode': 'draftcode', 'orgname': 'institutionname'},
    'rh_billdiscount': {'contractcode': 'billcode', 'orgname': 'institutionname'},
    'rh_billdiscount_d': {'contractcode': 'billcode', 'orgname': 'institutionname'},
    'rh_billdiscount_f': {'contractcode': 'billcode', 'orgname': 'institutionname'},
}

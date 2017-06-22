#!C:\Python27\python.exe
# coding: utf-8

__author__ = 'yueyt'

import datetime
from spider_app.html_downloader import RedisOp
from config_tt import base_config
import os
redis_conn = RedisOp(**base_config.redis_config)

# 获取查询的上季度参数
def get_last_quarter():
    current_date = datetime.date.today()
    if current_date.month < 4:
        return (datetime.date(current_date.year - 1, 10, 1).strftime('%Y-%m-%d'),
                datetime.date(current_date.year - 1, 12, 31).strftime('%Y-%m-%d'))
    elif current_date.month < 7:
        return (datetime.date(current_date.year, 1, 1).strftime('%Y-%m-%d'),
                datetime.date(current_date.year, 3, 31).strftime('%Y-%m-%d'))
    elif current_date.month < 10:
        return (datetime.date(current_date.year, 4, 1).strftime('%Y-%m-%d'),
                datetime.date(current_date.year, 6, 30).strftime('%Y-%m-%d'))
    else:
        return (datetime.date(current_date.year, 7, 1).strftime('%Y-%m-%d'),
                datetime.date(current_date.year, 9, 30).strftime('%Y-%m-%d'))


# last_quarter_start, last_quarter_end = get_last_quarter()
#'2015-07-01', '2015-09-30','2015-10-01', '2015-12-31','2016-01-01', '2016-03-31','2016-04-01','2016-06-30'
last_quarter_start, last_quarter_end = '2016-04-01','2016-06-30'
# last_quarter_start = redis_conn.run_redis_fun('hget','rh_search_date_range','last_quarter_start').decode()
# last_quarter_end = redis_conn.run_redis_fun('hget','rh_search_date_range','last_quarter_end').decode()
# print(last_quarter_start,last_quarter_end)
if os.getenv('last_quarter_start'):
    last_quarter_start = os.getenv('last_quarter_start')
if os.getenv('last_quarter_end'):
    last_quarter_end = os.getenv('last_quarter_end')

current_date = datetime.date.today().strftime('%Y-%m-%d')

# 确定借款人
orgcodeinfo_list_payload = dict(
    type='00101',
    nocaCode='1',
    sdeporgcode='',
    queryreason='03',
    # next list
    _RollTaskID=None,
    canSearch=None,
    whereClause=None,
    currentPage=None,
    pageCount=None,
    pageSize=None,
    totalCount=None,
)
# 用中征码来爬取
loancardno_list_payload = dict(
    type='00101',
    nocaCode='1',
    creditcode='',
    loancardno='',
    sdeporgcode='',
    registertype='',
    registercode='',
    sdepnationaltaxcode='',
    sdeplandtaxcode='',
    queryreason='03',
    # next list
    _RollTaskID=None,
    canSearch=None,
    whereClause=None,
    currentPage=None,
    pageCount=None,
    pageSize=None,
    totalCount=None,
)
# 机构查询
orgcodeinfo_list_title = ['orgname', 'mecreditcode', 'orgcode', 'midsigncode', 'regtype', 'regnum', 'staxidnum',
                          'ltaxidnum', ]

# 当前综合信息
detail_qt_payload = dict(
    crccode='',
    attribute='1',
    borrnatucode='1',
    loancard='',
    curtype='00101',
    somePage='',
)

# 余额信息
balancetypesum_list_payload = dict(
    systemDate=current_date,
    owesendtime=last_quarter_end,
    checkboxa0='on',
    loansign='on',
    suchloan='on',
    keepfinancingsign='on',
    financingsign='on',
    discountsign='on',
    creditsign='on',
    acceptordersign='on',
    keepcasesign='on',
    peeloffsign='on',
    loancard='',
    searchtype='balance',
    owesendtime1='null',
    rmb='',
    dollar='',
    total='',
    typecode='%s',
    borrowernamecn='',
    # next list
    _RollTaskID=None,
    canSearch=None,
    whereClause=None,
    currentPage=None,
    pageCount=None,
    pageSize=None,
    totalCount=None,
)
# 余额信息（各个分支需要提交的表单）
balancetypesum_list_payload_detail = dict(
    systemDate=current_date,
    owesendtime=last_quarter_end,
    checkboxa0='on',
    loansign='on',
    suchloan='on',
    keepfinancingsign='on',
    financingsign='on',
    discountsign='on',
    creditsign='on',
    acceptordersign='on',
    keepcasesign='on',
    peeloffsign='on',
    loancard='',
    searchtype='balance',
    owesendtime1=last_quarter_end,
    rmb='',
    dollar='',
    total='',
    typecode='%s',
    borrowernamecn='',
    # next list
    _RollTaskID=None,
    canSearch=None,
    whereClause=None,
    currentPage=None,
    pageCount=None,
    pageSize=None,
    totalCount=None,
)
# balancetypesum_list_payload = {
#     'systemDate':current_date,
#     'owesendtime':last_quarter_end,
#     'checkboxa0':'on',
#     'loansign':'',
#     'suchloan':'',
#     'keepfinancingsign':'',
#     'financingsign':'',
#     'discountsign':'',
#     '':'','':'','':'','':'','':'','':'','':'','':''}
# 余额汇总表
# 类型  人民币(元) 外币折美元(元) 本外币折人民币(元)
balancetypesum_detail_title = ['typename', 'rmb', 'dollars', 'dollarstormb']

# 贷款
# 合同号码 生效日期 终止日期 币种 贷款余额 金融机构名称 合同有效状态
loaninfo_list_title = ['contractnumber', 'startdate', 'enddate', 'currencytype', 'balanceloan',
                       'financialinstitution', 'loanstate']

# 贷款合同号码  3360102013M100014200  金融机构代码
#  33703010119
# 金融机构名称 交通银行股份有限公司绍兴延安路支行
# 借款人名称  浙江雅杰尔包装有限公司
# 中征码  3306000000375162 授信协议号码  MC156CMIS300498135
# 合同金额币种 人民币 贷款合同金额  4,000,000.00 可用余额 0.00
# 贷款合同生效日期  2013-12-20 贷款合同终止日期  2014-06-20
# 银团标志  否 担保标志  是
# 贷款合同有效状态  是
loaninfo_detail_title = ['contractnumber', 'institutioncode', 'financialinstitution', 'borrowername', 'midsigncode',
                         'creditagreementnumber', 'currencytype', 'loanbalance', 'availablebalance', 'startdate',
                         'enddate', 'syndicatedlogo', 'guaranteetag', 'loanstate', ]

# 借据编号	币种	借据金额(元)	借据余额(元)	放款日期	到期日	五级分类	业务发生日期
iouinfo_list_title = ['ioucode', 'currencytype', 'iocamount', 'balance', 'loandate', 'expirationdate', 'gradename',
                      'businessdate']
# 借据详情
# 借据编号  0211012537160726000100
# 币种 人民币  借据金额（元）  1,000,000,000.00 借据余额（元）  1,000,000,000.00
# 放款日期  2016-07-26  到期日  2017-07-25
# 贷款形式  新增贷款  贷款性质  自营贷款
# 贷款投向  其他未列明建筑业  贷款种类  短期流动资金贷款
# 五级分类  正常  四级分类
# 展期标志  否
iouinfo_detail_title = ['ioucode', 'currencytype', 'iocamount', 'balance', 'loandate', 'expirationdate', 'loanform',
                        'loancharacter', 'loanorientation', 'loantype', 'gradename', 'fourgrade', 'showtag', ]
# 还款
# 还款次数 还款日期 还款金额（元） 还款方式
repaymentinfo_list_title = ['repaynumber', 'repaydate', 'repayamount', 'repaymethod']

# 展期
# 展期次数 展期起始日 展期到期日 展期金额（元）
extensioninfo_list_title = ['extensionnumber', 'extensionfrom', 'extensionto', 'extensionmoney']

# 保证合同编号 3360102013AM00007600  保证合同有效标志  是
# 币种 人民币 保证合同金额 26,000,000.00
# 业务发生金融机构名称 交通银行股份有限公司绍兴延安路支行  保证合同签订日期 2013-07-04
# 保证担保形式 单人担保
guaranteecontractinfo_detail_title = ['contractencoding', 'contractvalidstate', 'currencytype', 'contractamount',
                                      'institutionname', 'signingdate', 'guaranteeform']

# 自然人保证人信息
# 保证人名称 保证人证件类型 保证人证件号码 该保证人保证担保金额 币种
guaranteinfo_person_list_title = ['guarantorname', 'guarantorcardtype', 'guarantorcard', 'guarantoraccount',
                                  'currencytype']
# 保证人名称 保证人中征码 该保证人保证担保金额 币种
guaranteinfo_list_title = ['guarantorname', 'guarantormidcode', 'guarantoraccount', 'currencytype']

# 抵押合同编号 3360102013AF00007600  合同有效标志  是
# 币种 人民币  抵押合同金额 12,000,000.00
# 业务发生金融机构名称 交通银行股份有限公司绍兴延安路支行  抵押合同签订日期 2013-07-04
mortgagecontract_detail_title = ['mortcontractcode', 'contractstate', 'currencytype', 'mortgconamount',
                                 'institutionname', 'businesssigntime']
# 自然人抵押信息
# 抵押人名称 抵押人证件类型 抵押人证件号码 该抵押人抵押担保金额 币种
mortgageinfo_person_list_title = ['mortgagename', 'mortcardtype', 'mortcard', 'guarantoramount', 'currencytype']
# 被担保自然人保证人列表信息
#  保证人名称  保证人证件类型  保证人证件号码  该保证人保证担保金额  币种
rh_guarantor_person = ['guarantorname', 'guarantorcardtype', 'guarantorcard', 'guarantamout', 'currencytype']
# 被担保保证人列表信息
#  保证人名称  保证人中征码  该保证人保证担保金额  币种
# 被担保合同对应主业务汇总信息
#  业务类型  业务发生额  业务余额
rh_bdbbusinesssum = ['businesstype', 'businessoccurrence', 'businessbalance']
rh_guarantor = ['guarantorname', 'guarantormidcode', 'guarantamout', 'currencytype']
# 被担保合同对应主业务汇总详细信息 ()
#  主业务号码  主业务业务发生额  主业务业务余额  币种  主业务结清状态  五级分类
rh_bdbbusiness = ['guaranteenumber', 'mainbusamount', 'mainbusblance', 'currencytype', 'mainbusinessstate', 'fivegrade']
# 抵押人名称 抵押人中征码 该抵押人抵押担保金额 币种
mortgageinfo_list_title = ['mortgagename', 'mortmidcode', 'guarantoramount', 'currencytype']
# 抵押人中征码(抵押人证件号码) 抵押序号 抵押金额 抵押币种 抵押物评估价值 抵押物评估币种
# 评估日期 评估机构名称 评估机构组织机构代码 抵押物种类
# 登记机关 登记日期 抵押物说明 业务发生日期
mortcontractinfo_list_title = ['mortmidcode', 'mortgageid', 'mortgageamount', 'currencytype', 'collassvalue',
                               'collcurrencytype',
                               'assdate', 'evalmech', 'orgcode', 'colltype',
                               'signdept', 'signdate', 'collmome', 'businessdate']
# 质押合同概要信息(rh_borrowerpledgeinfo)
#  质押合同编号  合同有效标志  币种  质押合同金额  业务发生金融机构  质押合同签订日期
rh_borrowerpledgeinfo = ['pledgecode', 'validstate', 'currencytype', 'contractamount', 'businessinst', 'signingdate']
pledgemomelist_detail_title = []
# 自然人质押人信息(rh_pledgemome_person)
#  质押人名称  质押人证件类型  质押人证件号码  该质押人质押担保金额  币种
rh_pledgemome_person = ['pledgename', 'borrowercardtype', 'borrowercard', 'pledgeaccount', 'currencytype']
# 余额信息-》质押人信息()
#  质押人名称  质押人中征码  该质押人质押担保金额  币种
rh_pledgemome = ['pledgename', 'pledgemidcode', 'pledgeaccount', 'currencytype']
# 质押物信息()
#  质押人中征码(质押人证件号码)  质押序号  质押金额  质押币种  质押物估计价值  质押物价值币种  质押物种类
rh_pledgemomelist = ['pledgemidcode', 'pledgeid', 'pledgeaccount', 'currencytype', 'pledgevaluation', 'currencytype2',
                     'pledgetype', 'businessdate']
# 保函
guarantee_list_title = ['guaranteecode', 'guaranteetype', 'starttime', 'endtime', 'currencytype', 'guaranteebalance',
                        'institutionname', 'fivegrade', ]
guarantee_detail_title = ['guaranteecode', 'institutionname', 'institutioncode', 'borrowername', 'midsigncode',
                          'guaranteetype', 'guaranteestate', 'currencytype', 'guaranteeaccount', 'starttime', 'endtime',
                          'marginratio', 'blancedate', 'guaranteebalance', 'guaranteesign', 'fivegrade',
                          'advancesign', ]
# 保理
# 保理协议编号 叙做日期 币种 叙做余额 金融机构名称 四级分类 五级分类
factoringinfo_list_title = ['factoringcode', 'sydate', 'currencytype', 'syamount', 'institutionname', 'fourgrade',
                            'fivegrade']

# 保理协议编号  4612014001019000 金融机构名称  交通银行股份有限公司海口龙昆南支行
# 金融机构代码  6410301K700 保理产品类型  国内卖方保理融资
# 保理业务状态  正常 借款人名称  海南金鹿投资集团有限公司
# 借款人中征码  4601000000452474 币种  人民币
# 叙做金额  550,000.00 叙做日期  2014-06-27
# 叙做余额  550,000.00 余额变化日期  2015-08-16
# 担保标志  是 五级分类  正常
# 四级分类   垫款标志  否
factoringinfo_detail_title = ['factoringcode', 'institutionname', 'institutioncode', 'factoringtype', 'factoringstyle',
                              'borrowername', 'borrowermidsigncode', 'currencytype', 'syamount', 'sydate', 'syblance',
                              'blancedate', 'guaranteesign', 'fivegrade', 'fourgrade', 'advancesign']

# 融资余额
# 协议编号 协议生效日期 协议终止日期 币种 融资余额 金融机构名称 协议有效状态
fagreementinfo_list_title = ['financecode', 'starttime', 'endtime', 'currencytype', 'financeingbalance',
                             'institutionname', 'effectivestate']
# 融资协议编号 HETO110650000201600437
# 金融机构名称 ****** 金融机构代码 ******
# 借款人名称 中农集团控股股份有限公司  中征码 1101020004074240
# 融资协议币种  人民币   融资协议金额  42,642,500.00  融资协议余额  42,642,500.00
# 融资协议生效日期  2016-08-31  融资协议终止日期  2017-02-20
# 担保标志  否  融资协议有效状态  是
fagreementinfo_detail_title = ['financecode', 'institutionname', 'institutioncode', 'borrowername', 'midsigncode',
                               'currencytype', 'financeaccount', 'financeblance', 'starttime', 'endtime',
                               'guaranteesign', 'effectivestate']

# 融资业务信息
# 融资业务编号 币种 融资业务金额(元) 融资业务余额(元) 发放日期 结束日期 五级分类 业务发生日期
financebusiness_list_title = ['financebussinesscode', 'currencytype', 'financeaccount', 'financeblance', 'starttime',
                              'endtime',
                              'businessdate']
# 融资业务编号  910GFC1600063   融资业务种类  进口押汇
# 币种 人民币  融资业务金额（元）  16,750,000.00 融资业务余额（元）  16,750,000.00
# 发放日期  2016-05-04  结束日期  2016-10-31
# 展期标志  否  五级分类  正常  四级分类  正常
financebusiness_detail_title = ['financebussinesscode', 'financetype', 'currencytype', 'financeaccount',
                                'financeblance',
                                'starttime', 'endtime', 'identification', 'fivegrade', 'fourgrade']

# 票据贴现（未结清金额）
# 票据内部编号 pj1144730 票据种类 银行承兑汇票
# 贴现金融机构名称 ****** 贴现金融机构代码 ******
# 贴现申请人名称 中农集团控股股份有限公司 贴现申请人中征码 1101020004074240
# 承兑人/行名称  承兑人/行卡号
# 贴现币种 人民币 贴现金额 10,000,000.00
# 贴现日 2015-08-20 承兑到期日 2016-02-11
# 票面金额 10,000,000.00 票据状态 正常
# 五级分类 正常 四级分类
billdiscount_detail_title = ['billcode', 'tickettype', 'institutionname', 'institutioncode', 'applicant',
                             'applicantmidsigncode', 'bankname', 'bankcode', 'currencytype', 'discountamount',
                             'discountdate', 'acceptancedate', 'parvalue', 'billstate', 'fivegrade', 'fourgrade']

# 承兑汇票（未结清金额）
# 承兑协议号码 汇票号码 汇票承兑日 汇票到期日 币种 汇票金额 金融机构名称 五级分类
draft_list_title = ['draftagreementcode', 'draftcode', 'acceptancedate', 'draftenddate', 'currencytype', 'draftaccount',
                    'institutionname', 'fivegrade']
# 承兑协议号码 2016083000000022 汇票号码 299858
# 金融机构名称 ****** 金融机构代码 ******
# 出票人名称 中农集团控股股份有限公司 出票人中征码 1101020004074240
# 汇票币种 人民币 汇票出票金额 1,000,000.00
# 五级分类  正常 汇票到期日 2017-02-28
# 汇票签发日 2016-08-30 汇票付款日期 2017-02-28
# 保证金比例(%)  25 担保标志  否
# 汇票状态  正常 垫款标志  否
draft_detail_title = ['draftagreementcode', 'draftcode', 'institutionname', 'institutioncode', 'drawername',
                      'drawermidsigncode', 'currencytype', 'draftaccount', 'fivegrade', 'draftenddate', 'signtime',
                      'draftdate', 'marginratio', 'guaranteesign', 'draftstate', 'advancesign']
# 信用证余额
# 信用证号码 开证日期 信用证有效期 币种 信用证余额 金融机构名称 五级分类
creditbalance_list_title = ['creditcode', 'issuingdate', 'creditvalidperiod', 'currencytype', 'creditcardblance',
                            'institutionname', 'institutioncode']
creditbalance_detail_title = ['creditcode', 'institutionname', 'institutioncode', 'borrowername', 'midsigncode',
                              'currencytype', 'issuingblance', 'issuingdate', 'creditvalidperiod', 'payperiod',
                              'marginratio', 'creditreptdate', 'creditcardblance', 'fivegrade', 'guaranteetag',
                              'creditstate', 'creditoutdate', 'advident']
# 类贷款余额
# 合约号码  LS2009-d92a89c4-c7b7-4941-8990-f0731332e4ed  授信机构代码  ******
# 授信机构名称 ******
# 企业名称  云南省公路开发投资有限责任公司
# 中征码  5301010001156713
# 合约金额币种 人民币 合约金额  450,000,000.00 可用余额 0.00
# 合约生效日期  2010-09-10 合约终止日期  2020-12-09
# 合约有效状态  是 担保标志  否
specialloaninfo_detail_title = ['contractnumber', 'institutioncode', 'financialinstitution', 'specialloanname',
                                'midsigncode', 'currencytype', 'specialloanbalance', 'availablebalance', 'startdate',
                                'enddate', 'loanstate', 'guaranteetag']

#  融资编号  币种  融资金额（元）  余额（元）  融资日期  到期日   五级分类/交易状态  业务发生日期
rh_financebusiness_loan_detail = ['financecode', 'currencytype', 'financeaccount', 'financeblance', 'starttime',
                                  'endtime', 'fivegrade', 'businessdate']
# 类贷款融资信息()
#  融资编号  币种  融资金额（元）  余额（元）  融资日期  到期日  形式
#  性质  投向  业务种类  五级分类/交易状态  是否延期
rh_financebusiness_loan = ['financecode', 'currencytype', 'financeaccount', 'financeblance', 'starttime', 'endtime',
                           'financeform', 'financecharacter', 'financeorientation', 'financetype', 'fivegrade',
                           'identification']

# 担保信息
# 对外担保信息汇总:assuretype='outassure'
# 被担保信息汇总:assuretype='byassure'
guaranteesum_list_payload = dict(
    borrowernamecn='',
    loancard='',
    attribute='1',
    systemDate=current_date,
    assure='curassure',
    assuretype='%s',
    endtime='',
    guarant='guarant',
    pledge='pledge',
    impawn='impawn',
    # next list
    _RollTaskID=None,
    canSearch=None,
    whereClause=None,
    currentPage=None,
    pageCount=None,
    pageSize=None,
    totalCount=None,
)
# 对外担保
outguarantee_list_payload = dict(
    borrowernamecn='',
    loancard='',
    attribute='1',
    systemDate=current_date,
    assure='curassure',
    assuretype='outassure',
    type='%s',
    endtime='',
    guarant='guarant',
    pledge='pledge',
    impawn='impawn',
    # next list
    _RollTaskID=None,
    canSearch=None,
    whereClause=None,
    currentPage=None,
    pageCount=None,
    pageSize=None,
    totalCount=None,
)
# 被担保
bguarantee_list_payload = dict(
    borrowernamecn='',
    loancard='',
    attribute='1',
    systemDate=current_date,
    assure='curassure',
    assuretype='byassure',
    type='%s',
    endtime='',
    guarant='guarant',
    pledge='pledge',
    impawn='impawn',
    # next list
    _RollTaskID=None,
    canSearch=None,
    whereClause=None,
    currentPage=None,
    pageCount=None,
    pageSize=None,
    totalCount=None,
)
# 担保保证合同信息
# 保证合同编号 015004086701
# 保证合同金额 200,000,000.00 币种 人民币
# 本担保人保证担保金额 200,000,000.00 本担保人保证担保金额计量币种 人民币
# 业务发生金融机构名称 ****** 保证合同有效状态  是
# 保证合同签订日期  2015-05-07  保证担保形式  单人担保
# dbguaranteecontract_detail_title = ['guaranteecode', 'guaranteeblance', 'currencytype', 'guaranteemoney',
#                                     'gmoneytype', 'institutionname', 'guaranteestate', 'signdate',
#                                     'guaranteemothed', ]
dbguaranteecontract_detail_title = ['guaranteecode', 'guaranteeblance', 'currencytype', 'guaranteemoney',
                                    'gmoneytype', 'institutionname', 'guaranteestate', 'signdate',
                                    'guaranteemothed', ]
duiwaidanbaoxinxi_payload = dict(
    loancardcode='',
    loanid='',
    loandb='',
    dzy='',
    financecode='',
    contractcode='',
    # /** loandb=1 担保  loandb=2 被担保  dzy=1 保证 2 抵押 3 质押**/

)
# 对外担保被担保人列表()
#  被担保人名称  被担保人中证码
rh_bdbenterprise = ['guarantorname', 'othermidsigncode']
# 对外担保合同对应主业务汇总信息 ()
#  业务类型  业务发生额  业务余额
rh_dbbusinesssum = ['businesstype', 'businessoccurrence', 'businessbalance']
# 对外担保合同对应主业务汇总详细信息()
#  主业务号码  主业务业务发生额  主业务业务余额  币种  主业务结清状态  借款人名称  五级分类
rh_dbbusiness = ['guaranteenumber', 'mainbusamount', 'mainbusblance', 'currencytype', 'mainbusinessstate',
                 'borrowername', 'fivegrade']
# 对外担保信息汇总
#  类型  本担保人担保金额（元）  本担保人担保金额本外币合计（元）
rh_outguaranteesum = ['guaranteetype', 'guarantoramount', 'additionalamount']
# 被担保信息汇总
#  类型  保证合同金额（元）  保证合同金额本外币合计（元）
rh_bdbguaranteesum = ['guaranteetype', 'guaranteeamount', 'additionalamount']
# 保证合同编号  110290000686504_0110200016-2016年吴江(保)字0092号
# 保证合同金额  6,200,000.00  币种  人民币
# 业务发生金融机构名称  ******  保证合同有效状态  是
# 保证合同签订日期  2016-02-24  保证担保形式  单人担保
bdbguaranteecontract_detail_title = ['guaranteecode', 'guaranteeamount', 'currencytype', 'institutionname',
                                     'guaranteestate', 'signdate', 'guaranteemothed']
# 被担保保证合同详细信息列表
#  序号  保证合同编号  保证合同有效状态  保证合同金额  币种  业务发生金融机构名称
rh_bdbguaranteecontractinfo_detail_title = ['number', 'guaranteecode', 'guaranteestate', 'guaranteeamount',
                                            'currencytype', 'institutionname']
# 抵押合同编号 D093302488
# 抵押合同金额 3,663,745,890.00 币种 人民币
# 本担保人抵押担保金额  3,663,745,890.00 本担保人抵押担保金额计量币种 人民币
# 业务发生金融机构名称 ****** 抵押合同有效状态  是
# 抵押合同签订日期  2009-06-30
dbmortinfo_detail_title = ['mortcode', 'mortamount', 'currencytype', 'guaranteeblance', 'guacurrencytype',
                           'institutionname', 'mortstate', 'signdate']
# -对外担保抵押合同详细信息
#  抵押合同编号  抵押合同金额  币种  本担保人抵押担保金额  本担保人抵押担保金额计量币种  业务发生金融机构名称  抵押合同有效状态  抵押合同签订时间
rh_dbmortinfo = ['mortcode', 'mortamount', 'currencytype', 'guaranteeamount', 'guacurrencytype', 'institutionname',
                 'mortstate', 'signdate']
# -对外担保抵押物详细信息(rh_dbmortmomelist)
#  抵押序号  抵押金额  币种  抵押物评估价值  抵押物评估币种  评估日期  评估机构名称
#  评估机构组织机构代码  抵押物种类  登记机关  登记日期  抵押物说明
rh_dbmortmomelist = ['mortgageid', 'mortgageamount', 'currencytype', 'collassvalue', 'collcurrencytype', 'assdate',
                     'evalmech',
                     'orgcode', 'colltype', 'signdept', 'signdate', 'collmome']
# 抵押合同编号 110290000686504_0110200016-2015年吴江(抵)字0436号
# 抵押合同金额 17,080,000.00 币种 人民币
# 业务发生金融机构名称 ****** 抵押合同有效状态  是
# 抵押合同签订日期  2015-08-28
securedmort_detail_title = ['securedmortcode', 'securedmortblance', 'currencytype', 'institutionname', 'securedstate',
                            'signdate']
# 被担保抵押合同详细信息
#   抵押合同编号  抵押合同金额  币种  业务发生金融机构名称  抵押合同有效状态  抵押合同签订日期
rh_bdbmortgagecontract = ['contractcode', 'contractamount', 'currencytype', 'institutionname', 'mortgagestate',
                          'signingdate']
# 被担保自然人抵押人列表信息(rh_bdbmortuser_person)
#  抵押人名称  抵押人证件类型  抵押人证件号码  该抵押人抵押担保金额  币种
rh_bdbmortuser_person = ['securedname', 'mortcardtype', 'mortcard', 'securedblance', 'currencytype']
#  质押合同编号  质押合同金额  币种  本担保人质押担保金额  本担保人质押担保金额计量币种
#  业务发生金融机构名称  质押合同状态  质押合同签订时间
dbpledgecontract_detail_title = ['pledgecode', 'pledgebalance', 'currencytype', 'guaranteeamount', 'guacurrencytype',
                                 'institutionname', 'pledgestate', 'signdate']
# 对外担保质押物详细信息
#  质押序号     质押金额  币种  质押物价值  质押物币种  质押物种类
rh_dbpledgemomelist = ['pledgeid', 'pledgeaccount', 'currencytype', 'pledgevaluation', 'currencytype2', 'pledgetype']
# 被担保抵押人列表信息(rh_bdbmortuser)
#  抵押人名称  抵押人中征码 该抵押人抵押担保金额  币种
rh_bdbmortuser = ['securedname', 'securedmidsigncode', 'securedblance', 'currencytype']
# 被担保抵押物信息()
#  抵押人中征码(抵押人证件号码)  抵押序号  抵押金额  抵押币种  抵押物评估价值  抵押物评估币种  评估日期
#  评估机构名称  评估机构组织机构代码  抵押物种类  登记机关  登记日期  抵押物说明  业务发生日期
rh_bdbmortcontractinfo = ['mortmidcode', 'mortgageid', 'mortgageamount', 'currencytype', 'collassvalue',
                          'collcurrencytype', 'assdate',
                          'evalmech', 'orgcode', 'colltype', 'signdept', 'signdate', 'collmome', 'businessdate']
# 质押合同编号 SubCon160713353510
# 质押合同金额 5,000,000.00 币种 人民币
# 业务发生金融机构名称 ****** 质押合同有效状态  是
# 质押合同签订日期  2016-07-13
bdbpledgecontract_detail_title = ['pledgecode', 'pledgebalance', 'currencytype', 'institutionname', 'pledgestate',
                                  'signdate']
# 被担保质押合同详细信息
#  质押合同编号  质押合同金额  币种  业务发生金融机构名称  质押合同有效状态  质押合同签订日期
rh_bdbpledgecontract = ['contractcode', 'contractamount', 'currencytype', 'institutionname', 'pledgestate',
                        'signingdate']
# 被担保质押人信息()
#  质押人名称  质押人中征码  该质押人质押担保金额  币种
rh_bdbpledgemome = ['pledgename', 'pledgemidcode', 'pledgeaccount', 'currencytype']
# 被担保自然人质押人信息(rh_bdbpledgemome_person)
#  质押人名称  质押人证件类型  质押人证件号码  该质押人质押担保金额  币种
rh_bdbpledgemome_person = ['pledgename', 'borrowercardtype', 'borrowercard', 'pledgeaccount', 'currencytype']
# 质押物信息()
#  质押人中征码(质押人证件号码) 质押序号  质押金额  质押币种  质押物估计价值  质押物价值币种  质押物种类  业务发生日期
rh_bdbpledgemomelist = ['pledgemidcode', 'pledgeid', 'pledgeaccount', 'currencytype', 'pledgevaluation',
                        'currencytype2', 'pledgetype', 'businessdate']

# 欠息信息
interestinfo_before_payload = dict(
    borrowernamecn='',
    loancard='',
    attribute='1',
    borrnatucode='1',
    crccode='',
    financecode='',
    datevalue='',
    debitflag='',
)

interestinfo_list_payload = dict(
    loancard='',
    borrowernamecn='',
    attribute='1',
    borrnatucode='1',
    debitflag='',
    queryendtime=last_quarter_end,
    # next list
    _RollTaskID=None,
    canSearch=None,
    whereClause=None,
    currentPage=None,
    pageCount=None,
    pageSize=None,
    totalCount=None,
)

# 金融机构名称 ****** 金融机构代码  ******
# 借款人名称 东群织造（苏州）有限公司  中征码 3202060000695361
# 币种 人民币 欠息余额 0.00
# 欠息类型 表内 欠息余额改变日期 2013-12-25
interestinfo_detail_title = ['institutionname', 'institutioncode', 'borrowername', 'midsigncode', 'currencytype',
                             'interestblance', 'interesttype', 'interestchangedate']

# 公开授信
creditagreeement_list_payload = dict(
    currentDate=current_date,
    systemDate=current_date,
    loancard='',
    attribute='null',
    borrowernamecn='',
    timepoint=last_quarter_end,
    # next list
    _RollTaskID=None,
    canSearch=None,
    whereClause=None,
    currentPage=None,
    pageCount=None,
    pageSize=None,
    totalCount=None,
)

# 授信协议号码 8731005981  金融机构代码  ******
# 金融机构名称 ******
# 借款人名称 云南省公路开发投资有限责任公司  中征码 5301010001156713
# 币种 人民币 授信额度 500,000,000.00
# 授信生效起始日期 2016-05-17  授信终止日期 2017-05-16
# 授信额度注销生效日期  授信额度注销原因
creditagreeement_detail_title = ['creditagreementnumber', 'institutioncode', 'institutionname', 'borrowername',
                                 'midsigncode',
                                 'currencytype', 'creditagreementmoney', 'creditagreementfrom', 'creditagreementto',
                                 'creditagreementoutdate', 'creditagreementoutinfo']

# 垫款信息
martpad_before_list_payload = dict(
    borrowernamecn='',
    loancard='',
    attribute='1',
    borrnatucode='1',
    crccode='',
    financecode='',
    datevalue='',
    debitflag='',
)
martpad_list_payload = dict(
    borrowernamecn='',
    loancard='',
    attribute='1',
    borrnatucode='1',
    debitflag='',
    queryendtime=last_quarter_end,
    # next list
    _RollTaskID=None,
    canSearch=None,
    whereClause=None,
    currentPage=None,
    pageCount=None,
    pageSize=None,
    totalCount=None,
)

# 垫款业务号码 70891  原业务号
#  70891
# 金融机构代码 ****** 金融机构名称 ******
# 借款人名称 中国建材股份有限公司  中征码 1101000001716976
# 垫款种类 承兑汇票垫款 垫款日期 2004-11-11
# 币种 人民币  垫款金额 4,374,000.00
# 垫款余额 0.00  余额发生日期 2004-11-11
# 四级分类 逾期天数在30天及以下  五级分类 正常
# 还款方式
martpad_detail_title = ['padcode', 'oldcode', 'institutioncode', 'institutionname', 'borrowername', 'midsigncode',
                        'padtype', 'paddate', 'currencytype', 'padamount', 'padbalance', 'padchangedate', 'fourgrade',
                        'fivegrade', 'rebackmethod']
# *不良负债信息,首页——————————----------------------------------------------------------------------------------------
#  类型 人民币（元）  外币折美元（元）  本外币折人民币（元）
rh_baddebtinfo = ['baddebt', 'rmb', 'dollars', 'dollarstormb']
baddebtinfo_list_payload = dict(
    systemDate=current_date,
    owesendtime=last_quarter_end,
    checkboxa0='on',
    loansign='on',
    suchloan='on',
    keepfinancingsign='on',
    financingsign='on',
    discountsign='on',
    creditsign='on',
    acceptordersign='on',
    keepcasesign='on',
    loancard='',
    searchtype='hadowe',
    owesendtime1=last_quarter_end,
    rmb='',
    dollar='',
    total='',
    typecode='',
    borrowernamecn='')
# *不良负债信息-->贷款余额（不良负债类贷款余额合约信息）
#  贷款合同号码  金融机构代码  金融机构名称  借款人名称 中征码
#  授信协议号码  合同金额币种  贷款合同金额  可用余额  贷款合同生效日期
#  贷款合同终止日期  银团标志  担保标志  贷款合同有效状态
rh_loaninfo_d = ['contractnumber', 'institutioncode', 'financialinstitution', 'borrowername', 'midsigncode',
                 'creditagreementnumber', 'currencytype', 'loanbalance', 'availablebalance', 'startdate',
                 'enddate', 'syndicatedlogo', 'guaranteetag', 'loanstate']
#  合同号码 生效日期 终止日期 币种 贷款余额 金融机构名称 贷款合同有效状态
rh_loaninfo_d_before = ['contractnumber', 'startdate', 'enddate', 'balancecurrency', 'balanceloan',
                        'financialinstitution', 'loanstate']
baddebtinfo_balance_payload = dict(
    systemDate=current_date,
    owesendtime=last_quarter_end,
    loancard='',
    searchtype='hadowe',
    owesendtime1=last_quarter_end,
    rmb='',
    dollar=0,
    total='',
    typecode='%s',
    borrowernamecn='',
)
# 不良负债信息->>贷款合同信息
#  贷款合同号码  金融机构代码  金融机构名称  借款人名称  中征码
#  授信协议号码  合同金额币种  贷款合同金额  贷款合同生效日期  贷款合同终止日期  银团标志、
#  担保标志  贷款合同有效状态

rh_fashenge_hetong_columns = ['contractnumber', 'institutioncode', 'financialinstitution', 'borrowername',
                              'midsigncode',
                              'creditagreementnumber', 'currencytype', 'loanbalance', 'startdate', 'enddate',
                              'syndicatedlogo',
                              'guaranteetag', 'loanstate']
# 不良负债信息->>>>不良负债融资协议信息
#  融资协议编号  金融机构名称  借款人姓名  中征码  融资协议币种
#  融资协议金额 融资协议余额  融资协议生效日期 融资协议终止日期 担保标志 融资协议有效状态
#  币种  融资余额
rh_fagreementinfo_d = ['financecode', 'institutionname', 'institutioncode', 'borrowername', 'midsigncode',
                       'currencytype',
                       'financeaccount', 'financeblance', 'starttime', 'endtime', 'guaranteesign', 'effectivestate',
                       'balancecurrencytype', 'financeingbalance']

# 不良负债信息->>>>不良负债借款人票据贴现详细信息
#  票据内部编号 票据种类  贴现金融机构名称 贴现金融机构代码 贴现申请人名称 贴现申请人中征码
#  承兑人/行名称 承兑人/行卡号 贴现币种 贴现金额 贴现日 承兑到期日  票面金额
#  票据状态  五级分类 四级分类
rh_billdiscount_d = ['billcode', 'tickettype', 'institutionname', 'institutioncode', 'applicant',
                     'applicantmidsigncode',
                     'bankname', 'bankcode', 'currencytype', 'discountamount', 'discountdate', 'acceptancedate',
                     'parvalue',
                     'billstate', 'fivegrade', 'fourgrade']
# 不良负债信息->>>>不良负债保理信息
#  保理协议编号  金融机构名称  金融机构代码  保理产品类型  保理业务状态
#  借款人名称  借款人中征码  币种  叙做金额  叙做日期  叙做余额  余额变化日期
#  担保标志  五级分类  四级分类   垫款标志
rh_factoringinfo_d = ['factoringcode', 'institutionname', 'institutioncode', 'factoringtype', 'factoringstyle',
                      'borrowername', 'borrowermidsigncode', 'currencytype', 'syamount', 'sydate', 'syblance',
                      'blancedate',
                      'guaranteesign', 'fivegrade', 'fourgrade', 'advancesign']
# 不良负债信息->>>>不良负债借款人信用证详细信息
#  信用证号码  金融机构名称  金融机构代码  借款人名称  中征码  开证币种
#  开证金额  开证日期  信用证有效期  付款期限  保证金比例  信用证余额报告日期
#  信用证余额  五级分类  担保标志  信用证状态  信用注销日期  垫款标志
rh_creditbalance_d = ['creditcode', 'institutionname', 'institutioncode', 'borrowername', 'midsigncode', 'currencytype',
                      'issuingblance', 'issuingdate', 'creditvalidperiod', 'payperiod', 'marginratio', 'creditreptdate',
                      'creditcardblance', 'fivegrade', 'guaranteetag', 'creditstate', 'creditoutdate', 'advident']

# 不良负债信息->>>>不良负债类贷款余额合约信息
#  合约号码  授信机构代码  授信机构名称  企业名称  中征码
#  合约金额币种  合约金额  可用余额  合约生效日期  合约终止日期  合约有效状态
#  担保标志  币种  融资余额
rh_specialloaninfo_d = ['contractnumber', 'institutioncode', 'financialinstitution', 'specialloanname', 'midsigncode',
                        'currencytype', 'specialloanbalance', 'availablebalance', 'startdate', 'enddate', 'loanstate',
                        'guaranteetag', 'balancecurrencytype', 'financeingbalance']
# 不良负债信息->>>>不良负债借款人承兑汇票详细信息
#  承兑协议号码  汇票号码  金融机构名称  金融机构代码  出票人名称  出票人中征码
#  汇票币种  汇票出票金额  五级分类  汇票到期日  汇票签发日/汇票出票日  汇票付款日期  保证金比例
#  担保标志  汇票状态  垫款标志
rh_draft_d = ['draftagreementcode', 'draftcode', 'institutionname', 'institutioncode', 'drawername',
              'drawermidsigncode',
              'currencytype', 'draftaccount', 'fivegrade', 'draftenddate', 'signtime', 'draftdate', 'marginratio',
              'guaranteesign', 'draftstate', 'advancesign']
# 不良负债信息->>>>不良负债借款人保函详细信息
#  保函号码  金融机构名称  金融机构代码  借款人名称  中征码  保函种类
#  保函状态  保函币种  保函金额  保函开立日期  保函到期日  保证金比例(%)  余额发生日期
#  保函余额  担保标志  五级分类  垫款标志
rh_guaranteeha_d = ['guaranteecode', 'institutionname', 'institutioncode', 'borrowername', 'midsigncode',
                    'guaranteetype',
                    'guaranteestate', 'currencytype', 'guaranteeaccount', 'starttime', 'endtime', 'marginratio',
                    'blancedate',
                    'guaranteebalance', 'guaranteesign', 'fivegrade', 'advancesign']

# *发生额信息,首页--------------------------------------------------------------------------------------------------------
#  类型  人民币(元)  外币折美元(元)  本外币折人民币合计(元)
rh_balancetypesum_f = ['typename', 'rmb', 'dollars', 'dollarstormb']
rh_fashenge_payload = dict(
    systemDate=last_quarter_end,  # last_quarter_end
    owesstarttime=last_quarter_start,  # last_quarter_start
    owesendtime=last_quarter_end,  # last_quarter_end
    checkboxa0='on',
    loansign='on',
    suchloan='on',
    keepfinancingsign='on',
    financingsign='on',
    discountsign='on',
    creditsign='on',
    acceptordersign='on',
    keepcasesign='on',
    peeloffsign='on',
    loancard='',
    searchtype='occur',
    owesstarttime1='null',
    owesendtime1=last_quarter_end,  # last_quarter_end
    rmb='',
    dollar='',
    total='',
    typecode='',
    borrowernamecn=''
)

rh_fashenge_below_payload = dict(
    systemDate=last_quarter_end,
    owesstarttime=last_quarter_start,  # last_quarter_start '2015-07-01'
    owesendtime=last_quarter_end,
    loancard='',
    searchtype='occur',
    owesstarttime1=last_quarter_start,  # last_quarter_start
    owesendtime1=last_quarter_end,
    rmb='',
    dollar='0',
    total='',
    typecode='%s',
    borrowernamecn='',
    #added by zhouj_123 20170525
    currentPage = None,
    pageCount = None,
    pageSize = None,
    totalCount = None
)
# *发生额信息-->>>>发生额贷款合同信息
#  贷款合同号码  金融机构代码  金融机构名称  借款人名称  中征码  授信协议号码
#  合同金额币种  贷款合同金额  贷款合同生效日期  贷款合同终止日期  银团标志  担保标志 贷款合同有效状态
rh_loaninfo_f = ['contractnumber', 'institutioncode', 'financialinstitution', 'borrowername', 'midsigncode',
                 'creditagreementnumber',
                 'currencytype', 'loanbalance', 'startdate', 'enddate', 'syndicatedlogo', 'guaranteetag', 'loanstate']
# *发生额信息-->>>>发生额保证合同概要信息
#  保证合同编号  保证合同有效状态  币种  保证合同金额  业务发生金融机构名称  保证合同签订日期
#  保证担保形式
rh_guaranteecontractinfo_f = ['contractencoding', 'contractvalidstate', 'currencytype', 'contractamount',
                              'institutionname', 'signingdate',
                              'guaranteeform']
# *发生额信息-->>>>发生额自然人保证人信息
#  保证人名称  保证人证件类型  保证人证件号码  该保证人保证担保金额 币种
rh_guaranteinfo_person_f = ['guarantorname', 'guarantorcardtype', 'guarantorcard', 'guarantoraccount', 'currencytype']
# *发生额信息-->>>>发生额保证人信息
#  保证人名称  保证人中征码  该保证人保证担保金额 币种
rh_guaranteinfo_f = ['guarantorname', 'guarantormidcode', 'guarantoraccount', 'currencytype']
# *发生额信息-->>>>发生额抵押合同概要信息
#  抵押合同编号  合同有效标志  币种  抵押合同金额
#  业务发生金融机构名称  抵押合同签订日期
rh_mortgagecontract_f = ['mortcontractcode', 'contractstate', 'currencytype',
                         'mortgconamount',
                         'institutionname', 'businesssigntime']
# *发生额信息-->>>>发生额自然人抵押人信息
#   抵押人名称  抵押人证件类型  抵押人证件号码  该抵押人抵押担保金额  币种
rh_mortgageinfo_person_f = ['mortgagename', 'mortcardtype', 'mortcard', 'guarantoramount', 'currencytype']
# *发生额信息-->>>>发生额抵押人信息
# 抵押人名称  抵押人中征码  该抵押人抵押担保金额  币种
rh_mortgageinfo_f = ['mortgagename', 'mortmidcode', 'guarantoramount', 'currencytype']
# *发生额信息-->>>>发生额抵押物信息
#  抵押人中征码(抵押人证件号码) 抵押序号  抵押金额  抵押币种  抵押物评估价值  抵押物评估币种
#  评估日期  评估机构名称  评估机构组织机构代码  抵押物种类  登记机关  登记日期  抵押物说明  业务发生日期
rh_mortcontractinfo_f = ['mortmidcode', 'mortgageid', 'mortgageamount', 'currencytype', 'collassvalue',
                         'collcurrencytype',
                         'assdate', 'evalmech', 'orgcode', 'colltype', 'signdept', 'signdate', 'collmome',
                         'businessdate']
# *发生额信息-->>>>发生额质押合同概要信息
#  质押合同编号  合同有效标志  币种  质押合同金额  业务发生金融机构
#  质押合同签订日期  开始时间  结束时间
rh_borrowerpledgeinfo_f = ['pledgecode', 'validstate', 'currencytype', 'contractamount', 'businessinst',
                           'signingdate']

# *发生额信息-->>>>发生额自然人质押人信息
#  质押人名称  质押人证件类型  质押人证件号码  该质押人质押担保金额  币种
#
rh_pledgemome_person_f = ['pledgename', 'borrowercardtype', 'borrowercard', 'pledgeaccount', 'currencytype', ]
# *发生额信息-->>>>发生额质押人信息
#  质押人名称  质押人中征码  该质押人质押担保金额  币种
rh_pledgemome_f = ['pledgename', 'pledgemidcode', 'pledgeaccount', 'currencytype']
# *发生额信息-->>>>发生额质押物信息
#  质押人中征码(质押人证件号码) 质押序号  质押金额  质押币种  质押物估计价值  质押物价值币种
#  质押物种类  业务发生日期
rh_pledgemomelist_f = ['pledgemidcode', 'pledgeid', 'pledgeaccount', 'currencytype', 'pledgevaluation', 'currencytype2',
                       'pledgetype', 'businessdate']
# *发生额信息-->>>>发生额借据信息
#  借据编号  币种  借据金额（元）  放款日期  到期日  贷款形式  贷款性质  贷款投向
#  贷款种类  五级分类  四级分类  展期标志  [业务发生日期(BUSINESSDATE)页面暂时找不到]
rh_iouinfo_f = ['ioucode', 'currencytype', 'iocamount', 'loandate', 'expirationdate', 'loanform', 'loancharacter',
                'loanorientation',
                'loantype', 'gradename', 'fourgrade', 'showtag']
# *发生额信息-->>>>发生额还款信息
#   还款次数  还款日期  还款金额（元）  还款方式
rh_repaymentinfo_f = ['repaynumber', 'repaydate', 'repayamount', 'repaymethod']
# *发生额信息-->>>>发生额展期信息/延期信息
#  中征码  借据编号/融资业务编号  展期次数/延期次数（类贷款融资业务）  展期起始日/延期起始日（类贷款融资业务） 展期到期日/延期到期日（类贷款融资业务）
#  展期金额（元）/延期金额（类贷款融资业务）  开始时间  结束时间
rh_extensioninfo_f = ['midsigncode', 'ioucode', 'extensionnumber', 'extensionfrom', 'extensionto',
                      'extensionmoney', 'starttime', 'endtime']
# *发生额信息-->>>>发生额融资协议信息
#  融资协议编号  金融机构名称  金融机构代码  借款人名称  中征码  融资协议币种
#  融资协议金额  融资协议生效日期  融资协议终止日期  担保标志  融资协议有效状态
rh_fagreementinfo_f = ['financecode', 'institutionname', 'institutioncode', 'borrowername', 'midsigncode',
                       'currencytype',
                       'financeaccount', 'financestarttime', 'financeendtime', 'guaranteesign', 'effectivestate']
# *发生额信息-->>>>发生额融资业务信息
#   融资业务编号  融资业务种类  币种  融资业务金额（元）
#  发放日期  结束日期  展期标志  五级分类  四级分类  业务发生日期
rh_financebusiness_f = ['financebussinesscode', 'financetype', 'currencytype', 'financeaccount',
                        'financestarttime', 'financeendtime', 'identification', 'fivegrade', 'fourgrade',
                        'businessdate']
#   融资业务编号 币种 融资业务金额(元) 融资业务余额(元) 发放日期 结束日期
#   五级分类 业务发生日期
rh_financebusiness_f_before = ['financebussinesscode', 'currencytype', 'financeaccount', 'financeblance', 'starttime',
                               'endtime',
                               'fivegrade', 'businessdate']
# *发生额信息-->>>>发生额借款人票据贴现详细信息
#  票据内部编号  票据种类  贴现金融机构名称  贴现金融机构代码  贴现申请人名称  贴现申请人中征码
#  承兑人/行名称  承兑人/行卡号  贴现币种  贴现金额  贴现日  承兑到期日  票面金额  票据状态
#  五级分类  四级分类
rh_billdiscount_f = ['billcode', 'tickettype', 'institutionname', 'institutioncode', 'applicant',
                     'applicantmidsigncode', 'bankname', 'bankcode', 'currencytype', 'discountamount', 'discountdate',
                     'acceptancedate', 'parvalue', 'billstate', 'fivegrade', 'fourgrade']
# *发生额信息-->>>>发生额保理信息
#  保理协议编号  金融机构名称  金融机构代码  保理产品类型  保理业务状态
#  借款人名称  借款人中征码  币种  叙做金额  叙做日期  担保标志
#  五级分类  四级分类  垫款标志
rh_factoringinfo_f = ['factoringcode', 'institutionname', 'institutioncode', 'factoringtype', 'factoringstyle',
                      'borrowername', 'borrowermidsigncode', 'currencytype', 'syamount', 'sydate', 'guaranteesign',
                      'fivegrade', 'fourgrade', 'advancesign']
# *发生额信息-->>>>发生额借款人信用证详细信息
#  信用证号码  金融机构名称  金融机构代码  借款人名称  中征码  开证币种  开证金额
#  开证日期  信用证有效期  付款期限  保证金比例  五级分类  担保标志
#  信用证状态  信用注销日期  垫款标志
rh_creditbalance_f = ['creditcode', 'institutionname', 'institutioncode', 'borrowername', 'midsigncode', 'currencytype',
                      'issuingblance', 'issuingdate', 'creditvalidperiod', 'payperiod', 'marginratio', 'fivegrade',
                      'guaranteetag', 'creditstate', 'creditoutdate', 'advident']
# *发生额信息-->>>>类贷款发生额合约信息      ************未找到有数据页面，暂和余额结构一致**************
#  合约号码  授信机构代码  授信机构名称  企业名称  中征码  合约金额币种
#  合约金额  可用余额  合约生效日期  合约终止日期  合约有效状态  担保标志
#  币种  融资余额  开始时间  结束时间
rh_specialloaninfo_f = ['contractnumber', 'institutioncode', 'financialinstitution', 'specialloanname', 'midsigncode',
                        'currencytype', 'specialloanbalance', 'availablebalance', 'startdate', 'enddate', 'loanstate',
                        'guaranteetag', 'balancecurrencytype', 'financeingbalance', 'starttime', 'endtime']
# *发生额信息-->>>>类贷款发生额融资信息      *************未找到有数据页面，暂和余额结构一致****************
#  中征码  融资编号  币种  融资金额（元）  余额（元）  融资日期
#  到期日  形式  性质  投向  业务种类  五级分类/交易状态
#  是否延期  开始时间  结束时间  合约号码  业务发生日期
rh_financebusiness_loan_f = ['midsigncode', 'financecode', 'currencytype', 'financeaccount', 'financeblance',
                             'financestarttime', 'financeendtime', 'financeform', 'financecharacter',
                             'financeorientation', 'financetype', 'fivegrade', 'identification', 'starttime', 'endtime',
                             'contractnumber', 'businessdate']
# *发生额信息-->>>>发生额借款人承兑汇票详细信息
#  承兑协议号码  汇票号码  金融机构名称  金融机构代码  出票人名称  出票人中征码
#  汇票币种  汇票出票金额  五级分类  汇票到期日  汇票签发日  汇票付款日期  保证金比例  担保标志
#  汇票状态  垫款标志  汇票承兑日
rh_draft_f = ['draftagreementcode', 'draftcode', 'institutionname', 'institutioncode', 'drawername',
              'drawermidsigncode', 'currencytype', 'draftaccount', 'fivegrade', 'draftenddate', 'signtime', 'draftdate',
              'marginratio', 'guaranteesign', 'draftstate', 'advancesign', 'acceptancedate']
#  承兑协议号码 汇票号码 汇票承兑日 汇票到期日 币种 汇票金额 金融机构名称 五级分类
rh_draft_befor = ['draftagreementcode', 'draftcode', 'acceptancedate', 'draftenddate', 'currencytype', 'draftaccount',
                  'institutionname', 'fivegrade']
# *发生额信息-->>>>发生额借款人保函详细信息
#  保函号码  金融机构名称  金融机构代码  借款人名称  中征码  保函种类  保函状态
#  保函币种  保函金额  保函开立日期  保函到期日  保证金比例(%)  担保标志
#  五级分类  垫款标志
rh_guaranteeha_f = ['guaranteecode', 'institutionname', 'institutioncode', 'borrowername', 'midsigncode',
                    'guaranteetype', 'guaranteestate', 'currencytype', 'guaranteeaccount', 'guarantstarttime',
                    'guarantendtime', 'marginratio', 'guaranteesign', 'fivegrade', 'advancesign']

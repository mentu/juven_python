#!C:\Python27\python.exe
# coding: utf-8
__author__ = 'yueyt'
import json

from config_tt import request_payload_config


# 解析并执行js函数
def premiseSubmit(typecode, rmb, dollar, total):
    if not total or total == '0.00':
        return
    else:
        return dict(typecode=typecode, rmb=rmb, dollar=dollar, total=total)


def premSubmit(crccode, loancard, borrnatucode):
    return dict(crccode=crccode, loancard=loancard, borrnatucode=borrnatucode)


def premise(asstype, type):
    return dict(type=type, assuretype=asstype)


def showRoll(taskID, canSearch, whereClause, currentPage, pageCount, pageSize, totalCount):
    return dict(
        _RollTaskID=taskID,
        canSearch=canSearch,
        whereClause=whereClause,
        currentPage=currentPage,
        pageCount=pageCount,
        pageSize=pageSize,
        totalCount=totalCount,
    )


# 处理流程配置表:页面下载器(downloader),下载器(parser),  数据保存器（saver）
processor = {
    # step1:  信用报告查询
    'orgcodeinfo': {
        # downloader
        'function': 'post_downloader',
        'url': 'newConfirmEditQuery.do',
        #'payload': request_payload_config.orgcodeinfo_list_payload,
        'payload': request_payload_config.loancardno_list_payload,
        # parser
        'parser_function': 'list_parser',
        'table_selector': 'table[cellpadding="4"] > tr',
        'table_header': True,
        'table_footer': False,
        # next & detail
        'detail_point': ['detail_qt'],
    },
    'saver': {
        'function': 'save_records',
    },
    # step2: 确定借款人 当前综合信息
    'detail_qt': {
        # downloader
        'function': 'onclick_downloader',
        'url': 'detail_qt_new.do',
        'payload': request_payload_config.detail_qt_payload,
        # parser
        'parser_function': 'null_parser',
        # next & detail
        #########################################################################################################
        # 主逻辑
        #
        # balancetypesum： 余额信息
        # rh_fashenge_befor_list 发生额信息
        # baddebtinfo_before_list 不良贷款信息
        # guaranteesum_before_list: 担保信息
        # interestinfosum_before_list： 欠息信息
        # creditagreeement_list； 公开授信
        # martpad_before_list：垫款信息
        #########################################################################################################
        'detail_point': ['balancetypesum', 'rh_fashenge_befor_list', 'baddebtinfo_before_list',
                         'guaranteesum_before_list',
                         'interestinfosum_before_list', 'creditagreeement_list', 'martpad_before_list'],
        # 'detail_point': ['guaranteesum_before_list'],#
    },
    # step3.1: 余额信息（该步骤可以忽略）
    'balancetypesum': {
        # downloader
        'function': 'post_downloader',
        'url': 'OweBalanceQueryAction.do',
        'payload': json.loads(json.dumps(request_payload_config.balancetypesum_list_payload)% ''),
        # parser
        'parser_function': 'list_parser',
        'ignore_detail_urls': True,
        'column_title': request_payload_config.balancetypesum_detail_title,
        'table': 'rh_balancetypesum',
        # next & detail
        #########################################################################################################
        # loaninfo_list： 贷款余额
        # specialloaninfo_list: 类贷款余额
        # factoringinfo_list：保理余额
        # fagreementinfo_list: 贸易融资余额
        # billdiscount_list:票据贴现（未结清金额）
        # draft_list: 承兑汇票（未结清金额）
        # creditbalance_list: 信用证余额
        # guarantee_list: 保函余额
        #########################################################################################################
        'detail_point': ['loaninfo_list', 'specialloaninfo_list', 'factoringinfo_list', 'fagreementinfo_list',
                         'billdiscount_list', 'draft_list', 'creditbalance_list', 'guarantee_list'],
        # 'detail_point': ['fagreementinfo_list'],
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    # step3.1.1: 贷款余额
    'loaninfo_list': {
        # downloader
        'function': 'post_downloader',
        'url': 'OweBalanceDetailAction.do',
        'payload': json.loads(json.dumps(request_payload_config.balancetypesum_list_payload_detail)%'1'),
        # parser
        'parser_function': 'list_parser',
        'table_header': True,
        'table_footer': True,
        'column_title': request_payload_config.loaninfo_list_title,
        'next_parama_list': ['balanceloan'],
        # next & detail
        'detail_point': ['loaninfo_detail'],
    },  # 贷款余额->贷款合同信息(rh_loaninfo)
    'loaninfo_detail': {
        # downloader
        'function': 'get_downloader',
        # parser
        'parser_function': 'detail_parser',
        'column_title': request_payload_config.loaninfo_detail_title,
        'table': 'rh_loaninfo',
        'curr_parama_list': ['balanceloan'],
        'next_parama_list': ['contractnumber'],
        # next & detail
        # 担保合同，抵押合同，质押合同，借据合同
        'detail_point': ['guaranteecontractinfo_list', 'mortgagecontract_list', 'pledgemomelist_list', 'iouinfo_list'],
        # 'detail_point': ['pledgemomelist_list'],
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    # step3.1.1.1: 借据
    'iouinfo_list': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'list_parser',
        'table_number': -1,
        'column_title': request_payload_config.iouinfo_list_title,
        'curr_parama_list': ['contractnumber'],
        'next_parama_list': ['contractnumber', 'businessdate'],
        # next
        'detail_point': ['iouinfo_detail'],
    },
    'iouinfo_detail': {
        # downloader
        'function': 'get_downloader',
        # parser
        'parser_function': 'detail_parser',
        'column_title': request_payload_config.iouinfo_detail_title,
        'table': 'rh_iouinfo',
        'curr_parama_list': ['contractnumber', 'businessdate'],
        'next_parama_list': ['ioucode'],
        # next
        'detail_point': ['repaymentinfo_list', 'extensioninfo_list'],
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    # step3.1.1.1.1: 还款信息
    'repaymentinfo_list': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'mix_list_parser',
        'table_number': 1,
        'column_title': request_payload_config.repaymentinfo_list_title,
        'table': 'rh_repaymentinfo',
        'curr_parama_list': ['ioucode'],
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    # step3.1.1.1.2: 展期信息
    'extensioninfo_list': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'mix_list_parser',
        'table_number': 2,
        'column_title': request_payload_config.extensioninfo_list_title,
        'table': 'rh_extensioninfo',
        'curr_parama_list': ['ioucode'],
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },

    # step3.1.1.2: 保证合同信息
    'guaranteecontractinfo_list': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'list_parser',
        'table_number': 2,
        'table_selector': 'table[cellspacing="1"]',
        'curr_parama_list': ['contractnumber', 'factoringcode', 'draftagreementcode', 'creditcode', 'guaranteecode','financecode'],
        'next_parama_list': ['contractnumber', 'factoringcode', 'draftagreementcode', 'creditcode', 'guaranteecode','financecode'],
        # next
        'detail_point': ['guaranteecontractinfo_detail'],
    },  # 保证合同信息->保证合同详细信息
    'guaranteecontractinfo_detail': {
        # downloader
        'function': 'get_downloader',
        # parser
        'parser_function': 'detail_parser',
        'column_title': request_payload_config.guaranteecontractinfo_detail_title,
        'table': 'rh_guaranteecontractinfo',
        # 贷款余额，保理余额
        'curr_parama_list': ['contractnumber', 'factoringcode', 'draftagreementcode', 'creditcode', 'guaranteecode','financecode'],
        'next_parama_list': ['contractencoding'],
        'rename_column_mapping': {'factoringcode': 'contractnumber', 'draftagreementcode': 'contractnumber',
                                  'creditcode': 'contractnumber', 'guaranteecode': 'contractnumber','financecode':'contractnumber'},
        # next  #1、自然人保证信息 2、保证人信息
        'detail_point': ['guaranteinfo_person_list', 'guaranteinfo_list'],
        # 'detail_point': ['guaranteinfo_list'],
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    # step3.1.1.2.1: 自然人保证信息
    'guaranteinfo_person_list': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'list_parser',
        'table_number': 2,
        'tr_select': 5,
        'column_title': request_payload_config.guaranteinfo_person_list_title,
        'table': 'rh_guaranteinfo_person',
        'curr_parama_list': ['contractencoding'],
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    # step3.1.1.2.2: 保证人信息
    'guaranteinfo_list': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'list_parser',
        'table_number': 3,
        'table_selector': 'table[align="center"]',
        'tr_select': 4,
        'table_header': True,
        'column_title': request_payload_config.guaranteinfo_list_title,
        'table': 'rh_guaranteinfo',
        'curr_parama_list': ['contractencoding'],
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    # step3.1.1.3: 抵押合同信息
    'mortgagecontract_list': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'list_parser',
        'table_number': 3,
        'table_selector': 'table[cellspacing="1"]',
        'curr_parama_list': ['contractnumber', 'factoringcode', 'draftagreementcode', 'creditcode', 'guaranteecode','financecode'],
        'next_parama_list': ['contractnumber', 'factoringcode', 'draftagreementcode', 'creditcode', 'guaranteecode','financecode'],
        # next
        'detail_point': ['mortgagecontract_detail'],
    },
    'mortgagecontract_detail': {
        # downloader
        'function': 'get_downloader',
        # parser
        'parser_function': 'detail_parser',
        'column_title': request_payload_config.mortgagecontract_detail_title,
        'table': 'rh_mortgagecontract',
        # 贷款余额，保理余额
        'curr_parama_list': ['contractnumber', 'factoringcode', 'draftagreementcode', 'creditcode', 'guaranteecode','financecode'],
        'rename_column_mapping': {'factoringcode': 'contractnumber', 'draftagreementcode': 'contractnumber',
                                  'creditcode': 'contractnumber', 'guaranteecode': 'contractnumber','financecode':'contractnumber'},
        'next_parama_list': ['mortcontractcode'],
        # next
        # 'detail_point': ['mortgageinfo_person_list', 'mortgageinfo_list', 'mortcontractinfo_list'],
        'detail_point': ['mortgageinfo_person_list', 'mortgageinfo_list', 'mortcontractinfo_list'],
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    # step3.1.1.3.1: 自然人-抵押人信息
    'mortgageinfo_person_list': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'person_parser',
        'table_number': 1,
        # 'table_header': True,
        # 'special_rows_tr_attrs': {'onclick': '', 'id': ''},#最初版的设置
        'special_rows_tr_attrs': {"onclick": "javascript:showDetail('detail0');"},
        'column_title': request_payload_config.mortgageinfo_person_list_title,
        'table': 'rh_mortgageinfo_person',
        'curr_parama_list': ['mortcontractcode'],
        'td_length': 5,
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    # step3.1.1.3.2: 抵押人信息
    'mortgageinfo_list': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'person_parser',
        'table_number': 1,
        'special_rows_tr_attrs': {"onclick": "javascript:showDetail('detail0');"},
        'column_title': request_payload_config.mortgageinfo_list_title,
        'table': 'rh_mortgageinfo',
        'curr_parama_list': ['mortcontractcode'],
        'next_parama_list': ['mortmidcode', 'mortcontractcode'],
        'ignore_detail_urls': True,
        'td_length': 4,
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    # step3.1.1.3.3: 抵押物信息  ->最初版的
    # 'mortcontractinfo_list': {
    #     # downloader
    #     'function': 'null_downloader',
    #     # parser
    #     'parser_function': 'list_parser',
    #     'table_number': 2,
    #     'table_selector': 'table[cellspacing="1"]',
    #     'column_title': request_payload_config.mortcontractinfo_list_title,
    #     'table': 'rh_mortcontractinfo',
    #     'curr_parama_list': ['mortcontractcode','mortmidcode'],
    #     # next
    #     'next_processor': 'saver',
    #     'add_searchdate':True,
    # },
    # # step3.1.1.3.3: 抵押物信息
    'mortcontractinfo_list': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'goods_parser',
        'table_selector': '#detail0 > td > table',
        'special_rows_tr_attrs': {"onclick": "javascript:showDetail('detail0');"},
        'column_title': request_payload_config.mortcontractinfo_list_title,
        'table': 'rh_mortcontractinfo',
        'curr_parama_list': ['mortcontractcode', 'mortmidcode'],
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    # step3.1.1.4: 质押合同信息
    'pledgemomelist_list': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'list_parser',
        'table_number': 4,
        'table_selector': 'table[cellspacing="1"]',
        'curr_parama_list': ['contractnumber', 'factoringcode', 'draftagreementcode', 'creditcode', 'guaranteecode','financecode'],
        'next_parama_list': ['contractnumber', 'factoringcode', 'draftagreementcode', 'creditcode', 'guaranteecode','financecode'],
        # next
        'detail_point': ['pledgemomelist_detail'],
    },  # 质押合同信息->质押合同详细信息
    'pledgemomelist_detail': {
        # downloader
        'function': 'get_downloader',
        # parser
        'parser_function': 'detail_parser',
        'column_title': request_payload_config.rh_borrowerpledgeinfo,
        'table': 'rh_borrowerpledgeinfo',
        'curr_parama_list': ['contractnumber','factoringcode', 'draftagreementcode', 'creditcode', 'guaranteecode','financecode'],
        'rename_column_mapping': {'factoringcode': 'contractnumber', 'draftagreementcode': 'contractnumber',
                                  'creditcode': 'contractnumber', 'guaranteecode': 'contractnumber','financecode':'contractnumber'},
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
        'next_parama_list': ['pledgecode',],
        'detail_point': ['rh_pledgemome_detail', 'rh_pledgemomelist_detail', 'rh_pledgemome_person_detail'],
        # 'detail_point': ['rh_pledgemomelist_detail_more'],
    },  # 质押合同信息->质押合同详细信息->自然质押人信息
    'rh_pledgemome_person_detail': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'person_parser',
        'table_number': 1,
        # 'table_header': True,
        # 'special_rows_tr_attrs': {'onclick': '', 'id': ''},#旧版本
        'special_rows_tr_attrs': {"onclick": "javascript:showDetail('detail0');"},
        'column_title': request_payload_config.rh_pledgemome_person,
        'table': 'rh_pledgemome_person',
        'curr_parama_list': ['pledgecode'],
        'td_length': 5,
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    # 质押合同信息->质押合同详细信息->质押人信息
    'rh_pledgemome_detail': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'person_parser',
        'table_selector': 'table#list',
        'table_number': 1,
        'special_rows_tr_attrs': {"onclick": "javascript:showDetail('detail0');"},
        'column_title': request_payload_config.rh_pledgemome,
        'table': 'rh_pledgemome',
        'curr_parama_list': ['pledgecode'],
        'td_length': 4,
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },  # 质押合同信息->质押合同详细信息-》+质押物信息
    # 'rh_pledgemomelist_detail':{
    #     # downloader
    #     'function': 'null_downloader',
    #     # parser
    #     'parser_function': 'list_parser',
    #     'table_selector': '#detail0 > td > table',
    #     'table_header':True,
    #     'column_title': request_payload_config.rh_pledgemomelist,
    #     'table': 'rh_pledgemomelist',
    #     'curr_parama_list': ['pledgecode'],
    #     # next
    #     'next_processor': 'saver',
    #     'add_searchdate':True,
    # },
    # 质押合同信息->质押合同详细信息-》+质押物信息
    'rh_pledgemomelist_detail': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'goods_parser',
        'table_selector': '#detail0 > td > table',
        'special_rows_tr_attrs': {"onclick": "javascript:showDetail('detail0');"},
        'column_title': request_payload_config.rh_pledgemomelist,
        'table': 'rh_pledgemomelist',
        'curr_parama_list': ['pledgecode'],
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    # step3.1.2: 保理余额
    'factoringinfo_list': {
        # downloader
        'function': 'post_downloader',
        'url': 'OweBalanceDetailAction.do',
        'payload': json.loads(json.dumps(request_payload_config.balancetypesum_list_payload_detail)%'2'),
        # parser
        'parser_function': 'list_parser',
        'table_header': True,
        'table_footer': True,
        # next & detail
        'detail_point': ['factoringinfo_detail'],
    },
    'factoringinfo_detail': {
        # downloader
        'function': 'get_downloader',
        # parser
        'parser_function': 'detail_parser',
        'column_title': request_payload_config.factoringinfo_detail_title,
        'table_selector': 'table#list > tr > td',
        'table': 'rh_factoringinfo',
        'next_parama_list': ['factoringcode'],
        # next
        'detail_point': ['guaranteecontractinfo_list', 'mortgagecontract_list', 'pledgemomelist_list'],
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    # step3.1.3: 贸易融资余额
    'fagreementinfo_list': {
        # downloader
        'function': 'post_downloader',
        'url': 'OweBalanceDetailAction.do',
        'payload': json.loads(json.dumps(request_payload_config.balancetypesum_list_payload_detail)%'3'),
        # parser
        'parser_function': 'list_parser',
        'table_header': True,
        'table_footer': True,
        'column_title': request_payload_config.fagreementinfo_list_title,
        'next_parama_list': ['financeingbalance'],
        # next & detail
        'detail_point': ['fagreementinfo_detail'],
    },
    'fagreementinfo_detail': {
        # downloader
        'function': 'get_downloader',
        # parser
        'parser_function': 'detail_parser',
        'column_title': request_payload_config.fagreementinfo_detail_title,
        'table': 'rh_fagreementinfo',
        'curr_parama_list': ['financeingbalance'],
        'next_parama_list': ['financecode'],
        # next
        'detail_point': ['guaranteecontractinfo_list', 'mortgagecontract_list', 'pledgemomelist_list',
                         'financebusiness_list'],
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    # step3.1.3.1: 融资业务信息
    'financebusiness_list': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'list_parser',
        'table_number': -1,
        'column_title': request_payload_config.financebusiness_list_title,
        'curr_parama_list': ['financecode'],
        'next_parama_list': ['financecode', 'businessdate'],
        # next
        'detail_point': ['financebusiness_detail'],
    },
    'financebusiness_detail': {
        # downloader
        'function': 'get_downloader',
        # parser
        'parser_function': 'detail_parser',
        'column_title': request_payload_config.financebusiness_detail_title,
        'table': 'rh_financebusiness',
        'curr_parama_list': ['financecode', 'businessdate'],
        'next_parama_list': ['financebussinesscode'],
        # next
        'detail_point': ['financebusiness_repaymentinfo_list', 'financebusiness_extensioninfo_list'],
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    # step3.1.3.1.1: 融资业务还款信息
    'financebusiness_repaymentinfo_list': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'list_parser',
        'table_number': 1,
        'column_title': request_payload_config.repaymentinfo_list_title,
        'table': 'rh_repaymentinfo',
        'curr_parama_list': ['financebussinesscode'],
        'rename_column_mapping': {'financebussinesscode': 'ioucode'},
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    # step3.1.3.1.2: 融资业务展期信息
    'financebusiness_extensioninfo_list': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'list_parser',
        'table_number': 2,
        'column_title': request_payload_config.extensioninfo_list_title,
        'table': 'rh_extensioninfo',
        'curr_parama_list': ['financebussinesscode'],
        'rename_column_mapping': {'financebussinesscode': 'ioucode'},
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    # step3.1.4: 票据贴现（未结清金额）
    'billdiscount_list': {
        # downloader
        'function': 'post_downloader',
        'url': 'OweBalanceDetailAction.do',
        'payload': json.loads(json.dumps(request_payload_config.balancetypesum_list_payload_detail)%'4'),
        # parser
        'parser_function': 'list_parser',
        'table_header': True,
        'table_footer': True,
        # next & detail
        'detail_point': ['billdiscount_detail'],
    },
    'billdiscount_detail': {
        # downloader
        'function': 'get_downloader',
        # parser
        'parser_function': 'detail_parser',
        'column_title': request_payload_config.billdiscount_detail_title,
        'table': 'rh_billdiscount',
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    # step3.1.5: 承兑汇票（未结清金额）
    'draft_list': {
        # downloader
        'function': 'post_downloader',
        'url': 'OweBalanceDetailAction.do',
        'payload': json.loads(json.dumps(request_payload_config.balancetypesum_list_payload_detail)%'5'),
        # parser
        'parser_function': 'list_parser',
        'table_header': True,
        'table_footer': True,
        'column_title': request_payload_config.draft_list_title,
        'next_parama_list': ['acceptancedate'],
        # next & detail
        'detail_point': ['draft_detail'],
    },
    'draft_detail': {
        # downloader
        'function': 'get_downloader',
        # parser
        'parser_function': 'detail_parser',
        'column_title': request_payload_config.draft_detail_title,
        'table': 'rh_draft',
        'curr_parama_list': ['acceptancedate'],
        'next_parama_list': ['draftagreementcode'],
        # next
        'detail_point': ['guaranteecontractinfo_list', 'mortgagecontract_list', 'pledgemomelist_list'],
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    # step3.1.6: 信用证余额
    'creditbalance_list': {
        # downloader
        'function': 'post_downloader',
        'url': 'OweBalanceDetailAction.do',
        'payload': json.loads(json.dumps(request_payload_config.balancetypesum_list_payload_detail)%'6'),
        # parser
        'parser_function': 'list_parser',
        'table_header': True,
        'table_footer': True,
        # next & detail
        'detail_point': ['creditbalance_detail'],
    },
    'creditbalance_detail': {
        # downloader
        'function': 'get_downloader',
        # parser
        'parser_function': 'detail_parser',
        'column_title': request_payload_config.creditbalance_detail_title,
        'table': 'rh_creditbalance',
        'next_parama_list': ['creditcode'],
        # next
        'detail_point': ['guaranteecontractinfo_list', 'mortgagecontract_list', 'pledgemomelist_list'],
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    # step3.1.7: 保函
    'guarantee_list': {
        # downloader
        'function': 'post_downloader',
        'url': 'OweBalanceDetailAction.do',
        'payload': json.loads(json.dumps(request_payload_config.balancetypesum_list_payload_detail)%'7'),
        # parser
        'parser_function': 'list_parser',
        'table_header': True,
        'table_footer': True,
        # next & detail
        'detail_point': ['guarantee_detail'],
    },
    'guarantee_detail': {
        # downloader
        'function': 'get_downloader',
        # parser
        'parser_function': 'detail_parser',
        'column_title': request_payload_config.guarantee_detail_title,
        'table': 'rh_guaranteeha',
        'next_parama_list': ['guaranteecode'],
        # next
        'detail_point': ['guaranteecontractinfo_list', 'mortgagecontract_list', 'pledgemomelist_list'],
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    # step3.1.9: 类贷款余额
    'specialloaninfo_list': {
        # downloader
        'function': 'post_downloader',
        'url': 'OweBalanceDetailAction.do',
        'payload': json.loads(json.dumps(request_payload_config.balancetypesum_list_payload_detail)%'9'),
        # parser
        'parser_function': 'list_parser',
        'table_header': True,
        'table_footer': True,
        # next & detail
        'detail_point': ['specialloaninfo_detail'],
    },
    'specialloaninfo_detail': {
        # downloader
        'function': 'get_downloader',
        # parser
        'parser_function': 'detail_parser',
        'column_title': request_payload_config.specialloaninfo_detail_title,
        'table': 'rh_specialloaninfo',
        'next_parama_list': ['contractnumber'],
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
        'detail_point': ['rh_financebusiness_loan_list'],
    },
    # 类贷款余额-> 类贷款融资信息
    'rh_financebusiness_loan_list': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'list_parser',
        'table_number': -1,
        'column_title': request_payload_config.rh_financebusiness_loan_detail,
        'curr_parama_list': ['contractnumber'],
        'next_parama_list': ['contractnumber', 'businessdate'],
        # next
        'detail_point': ['rh_financebusiness_loan_detail'],
    },
    'rh_financebusiness_loan_detail': {
        # downloader
        'function': 'get_downloader',
        # parser
        'parser_function': 'detail_parser',
        'column_title': request_payload_config.rh_financebusiness_loan,
        'table': 'rh_financebusiness_loan',
        'curr_parama_list': ['contractnumber', 'businessdate'],
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    # step3.2: 担保信息
    'guaranteesum_before_list': {
        # downloader
        'function': 'post_downloader',
        'url': 'AssureActionBefore.do',
        'payload': json.loads(json.dumps(request_payload_config.guaranteesum_list_payload) % 'outassure'),
        # parser
        'parser_function': 'null_parser',
        'table_header': True,
        # next and detail   #1、对外担保信息2、 被担保信息
        'detail_point': ['outguaranteesum_list', 'bguaranteesum_list'],
        # 'detail_point': ['bguaranteesum_list'],
    },
    # step3.2.1: 对外 担保信息
    # step3.2.1.x: 对外 担保信息->汇总信息
    'outguaranteesum_list': {
        # downloader
        'function': 'post_downloader',
        'url': 'AssureSumAction.do',
        'payload': json.loads(
            json.dumps(request_payload_config.guaranteesum_list_payload) % 'outassure'),
        'ignore_detail_urls': True,
        # parser
        'column_title': request_payload_config.rh_outguaranteesum,
        'table': 'rh_outguaranteesum',
        'parser_function': 'list_parser',
        'table_number': 0,
        'table_header': True,
        'next_processor': 'saver',
        'add_searchdate': True,
        # next and detail：1、对外担保汇总信息 2、保证 3、抵押 4、质押合同
        'detail_point': ['dbguaranteecontract_list', 'dbmortinfo_list',
                         'dbpledgecontract_list'],
        # 'detail_point': ['dbguaranteecontract_list'],
    },
    # step3.2.1.x: 对外 担保信息->汇总信息
    # 'outguaranteesum_detail': {
    #     # downloader
    #     'function': 'post_downloader',
    #     'url': 'AssureSumAction.do',
    #     'payload': json.loads(
    #         json.dumps(request_payload_config.guaranteesum_list_payload) % 'outassure'),
    #     # parser
    #     'column_title': request_payload_config.rh_outguaranteesum,
    #     'table': 'rh_outguaranteesum',
    #     'parser_function': 'list_parser',
    #     'table_number': 0,
    #     'table_header': True,
    #     'next_processor': 'saver',
    #     'add_searchdate': True,
    # },
    # step3.2.1.1: 保证合同列表信息
    'dbguaranteecontract_list': {
        # downloader
        'function': 'post_downloader',
        'url': 'AssureAllActionNew.do',
        'payload': json.loads(
            json.dumps(request_payload_config.outguarantee_list_payload) % '1'),
        # parser
        'parser_function': 'list_parser',
        'table_number': 0,
        'table_header': True,
        # next
        'detail_point': ['dbguaranteecontract_detail'],
    },  # 保证合同列表信息->保证合同详细信息
    'dbguaranteecontract_detail': {
        # downloader
        'function': 'get_downloader',
        # parser
        'parser_function': 'detail_parser',
        'column_title': request_payload_config.dbguaranteecontract_detail_title,
        'table': 'rh_dbguaranteecontract',
        'next_parama_list': ['guaranteecode'],
        'add_searchdate': True,
        # next
        'next_processor': 'saver',
        'detail_point': ['rh_bdbenterprise_detail', 'rh_dbbusinesssum_detail'],
        # 'detail_point':['rh_dbguaranteecontract_list'],
    },  # 保证合同列表信息->被担保人列表
    'rh_bdbenterprise_detail': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'list_parser',
        'table_number': 1,
        'table_header': True,
        'column_title': request_payload_config.rh_bdbenterprise,
        'table': 'rh_bdbenterprise',
        'curr_parama_list': ['guaranteecode'],
        'rename_column_mapping': {'guaranteecode': 'guaranteenumber'},
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },  # 保证合同列表信息->该担保合同对应主业务汇总信息
    'rh_dbbusinesssum_detail': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'list_parser',
        'table_selector': '.tablist',
        'curr_parama_list': ['guaranteecode'],
        'next_parama_list':['guaranteecode','businesstype'],
        'rename_column_mapping': {'guaranteecode': 'basecode'},
        'column_title': request_payload_config.rh_dbbusinesssum,
        'table': 'rh_dbbusinesssum',
        'ignore_detail_urls': 'test',
        'next_response':True,
        'add_searchdate': True,
        # next
        'next_processor': 'saver',
        'detail_point':['rh_dbguaranteecontract_list'],

    },  # 保证合同列表信息->该担保合同对应主业务汇总信息->对外担保保证合同详细信息(正则匹配出payload)
    'rh_dbguaranteecontract_list': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 're_add_post__parser',
        'curr_parama_list': ['guaranteecode','businesstype'],
        'next_parama_list': ['guaranteecode','businesstype'],
        'detail_point': ['rh_dbguaranteecontract_detail'],
        'next_response':True,
        'label_type':'1',
        'loandb_type':'1',
    },

    # 保证合同列表信息->该担保合同对应主业务汇总信息->对外担保保证合同详细信息
    'rh_dbguaranteecontract_detail': {
        # downloader
        'function': 'post_downloader',
        'url': 'AssureLoanKindDetailAction.do',
        'column_title': request_payload_config.rh_dbbusiness,
        'payload': request_payload_config.duiwaidanbaoxinxi_payload,
        'table': 'rh_dbbusiness',
        # parser
        'parser_function': 'list_parser',
        'curr_parama_list': ['guaranteecode','businesstype'],
        'rename_column_mapping': {'guaranteecode': 'basecode'},
        'table_number': 0,
        'table_header': True,
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    # step3.2.1.2: 抵押合同列表信息
    'dbmortinfo_list': {
        # downloader
        'function': 'post_downloader',
        'url': 'AssureAllActionNew.do',
        'payload': json.loads(
            json.dumps(request_payload_config.outguarantee_list_payload) % '2'),
        # parser
        'parser_function': 'list_parser',
        'table_header': True,
        # next
        'detail_point': ['dbmortinfo_detail'],
    },  # 对外担保信息->抵押->抵押合同详细信息
    'dbmortinfo_detail': {
        # downloader
        'function': 'get_downloader',
        # parser
        'parser_function': 'detail_parser',
        'column_title': request_payload_config.rh_dbmortinfo,
        'table': 'rh_dbmortinfo',
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
        'next_parama_list': ['mortcode'],
        # 1、对外担保抵押物详细信息 2\该担保合同对应主业务汇总信息
        'detail_point': ['rh_dbmortmomelist_detail','rh_dbbusinesssum_detail_1'],
        # 'detail_point': ['rh_dbbusinesssum_detail_1'],
    },  # 对外担保信息->抵押->抵押物详细列表信息
    'rh_dbmortmomelist_detail': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'list_parser',
        'table_number': 1,
        'table_header': True,
        'column_title': request_payload_config.rh_dbmortmomelist,
        'table': 'rh_dbmortmomelist',
        'curr_parama_list': ['mortcode'],
        'rename_column_mapping': {'mortcode': 'mortcontractcode'},
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },
# 该担保合同对应主业务汇总信息
    'rh_dbbusinesssum_detail_1': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'list_parser',
        'table_selector': '.tablist',
        'curr_parama_list': ['mortcode'],
        'next_parama_list':['mortcode','businesstype'],
        'rename_column_mapping': {'mortcode': 'basecode'},
        'column_title': request_payload_config.rh_dbbusinesssum,
        'table': 'rh_dbbusinesssum',
        'ignore_detail_urls': 'test',
        'next_response':True,
        'add_searchdate': True,
        # next
        'next_processor': 'saver',
        'detail_point':['rh_dbguaranteecontract_list_1'],

    },  # 保证合同列表信息->该担保合同对应主业务汇总信息->对外担保保证合同详细信息(正则匹配出payload)
    'rh_dbguaranteecontract_list_1': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 're_add_post__parser',
        'curr_parama_list': ['mortcode','businesstype'],
        'next_parama_list': ['mortcode','businesstype'],
        'detail_point': ['rh_dbguaranteecontract_detail_1'],
        'next_response':True,
        'label_type':'2',
        'loandb_type':'1',
    },

    # 保证合同列表信息->该担保合同对应主业务汇总信息->对外担保保证合同详细信息
    'rh_dbguaranteecontract_detail_1': {
        # downloader
        'function': 'post_downloader',
        'url': 'AssureLoanKindDetailAction.do',
        'column_title': request_payload_config.rh_dbbusiness,
        'payload': request_payload_config.duiwaidanbaoxinxi_payload,
        'table': 'rh_dbbusiness',
        # parser
        'parser_function': 'list_parser',
        'curr_parama_list': ['mortcode','businesstype'],
        'rename_column_mapping': {'mortcode': 'basecode'},
        'table_number': 0,
        'table_header': True,
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    # step3.2.1.3: 质押合同列表信息
    'dbpledgecontract_list': {
        # downloader
        'function': 'post_downloader',
        'url': 'AssureAllActionNew.do',
        'payload': json.loads(
            json.dumps(request_payload_config.outguarantee_list_payload) % '3'),
        # parser
        'parser_function': 'list_parser',
        'table_header': True,
        # next
        'detail_point': ['dbpledgecontract_detail'],
    },  # 对外担保信息->抵押->质押合同详细信息
    'dbpledgecontract_detail': {
        # downloader
        'function': 'get_downloader',
        # parser
        'parser_function': 'detail_parser',
        'column_title': request_payload_config.dbpledgecontract_detail_title,
        'table': 'rh_dbpledgecontract',
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
        'next_parama_list': ['pledgecode'],
        'detail_point': ['rh_dbpledgemomelist_detail','rh_dbbusinesssum_detail_2'],
        # 'detail_point': ['rh_dbbusinesssum_detail_2'],
    },  # 对外担保信息->抵押->对外担保质押物详细信息
    'rh_dbpledgemomelist_detail': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'list_parser',
        'table_number': 1,
        'table_header': True,
        'column_title': request_payload_config.rh_dbpledgemomelist,
        'table': 'rh_dbpledgemomelist',
        'curr_parama_list': ['pledgecode'],
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },
# 该担保合同对应主业务汇总信息
    'rh_dbbusinesssum_detail_2': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'list_parser',
        'table_selector': '.tablist',
        'curr_parama_list': ['pledgecode'],
        'next_parama_list':['pledgecode','businesstype'],
        'rename_column_mapping': {'pledgecode': 'basecode'},
        'column_title': request_payload_config.rh_dbbusinesssum,
        'table': 'rh_dbbusinesssum',
        'ignore_detail_urls': 'test',
        'next_response':True,
        'add_searchdate': True,
        # next
        'next_processor': 'saver',
        'detail_point':['rh_dbguaranteecontract_list_2'],

    },  #该担保合同对应主业务汇总信息->对外担保保证合同详细信息(正则匹配出payload)
    'rh_dbguaranteecontract_list_2': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 're_add_post__parser',
        'curr_parama_list': ['pledgecode','businesstype'],
        'next_parama_list': ['pledgecode','businesstype'],
        'detail_point': ['rh_dbguaranteecontract_detail_2'],
        'next_response':True,
        'label_type':'3',
        'loandb_type':'1',
    },

    # 保证合同列表信息->该担保合同对应主业务汇总信息->对外担保保证合同详细信息
    'rh_dbguaranteecontract_detail_2': {
        # downloader
        'function': 'post_downloader',
        'url': 'AssureLoanKindDetailAction.do',
        'column_title': request_payload_config.rh_dbbusiness,
        'payload': request_payload_config.duiwaidanbaoxinxi_payload,
        'table': 'rh_dbbusiness',
        # parser
        'parser_function': 'list_parser',
        'curr_parama_list': ['mortcode','businesstype'],
        'rename_column_mapping': {'mortcode': 'basecode'},
        'table_number': 0,
        'table_header': True,
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    # step3.2.2: 被担保信息
    # step3.2.2.x: 被担保信息->汇总信息
    'bguaranteesum_list': {
        # downloader
        'function': 'post_downloader',
        'url': 'AssureSumAction.do',
        'payload': json.loads(
            json.dumps(request_payload_config.guaranteesum_list_payload) % 'byassure'),
        # parser
        'parser_function': 'list_parser',
        'ignore_detail_urls': True,
        'table_number': 0,
        'table_header': True,
        'column_title': request_payload_config.rh_bdbguaranteesum,
        'table': 'rh_bdbguaranteesum',
        'next_processor': 'saver',
        'add_searchdate': True,
        # next and detail：1、被担保信息汇总 2、担保保证 3、抵押 4、质押合同
        'detail_point': ['bdbguaranteecontract_list', 'securedmort_list',
                         'bdbpledgecontract_list'],
        # 'detail_point': ['securedmort_list'],
    },
    # # step3.2.2.x: 被担保信息->汇总信息
    # 'bguaranteesum_detail': {
    #     # downloader
    #     'function': 'post_downloader',
    #     'url': 'AssureSumAction.do',
    #     'payload': json.loads(
    #         json.dumps(request_payload_config.guaranteesum_list_payload)%'byassure'),
    #     # parser
    #     'parser_function': 'list_parser',
    #     'table_number': 0,
    #     'table_header': True,
    #     'column_title': request_payload_config.rh_bdbguaranteesum,
    #     'table': 'rh_bdbguaranteesum',
    #     'next_processor': 'saver',
    #     'add_searchdate': True,
    # },
    # step3.2.2.1: 被担保保证合同列表信息
    'bdbguaranteecontract_list': {
        # downloader
        'function': 'post_downloader',
        'url': 'AssureAllActionNew.do',
        'column_title': request_payload_config.rh_bdbguaranteecontractinfo_detail_title,
        'payload': json.loads(
            json.dumps(request_payload_config.bguarantee_list_payload) % '1'),
        # parser
        'parser_function': 'list_parser',
        'next_parama_list': ['number'],
        'table_header': True,
        # next
        'detail_point': ['bdbguaranteecontract_detail'],
    },  # 被担保保证合同列表信息->详细信息
    'bdbguaranteecontract_detail': {
        # downloader
        'function': 'get_downloader',
        # parser
        'parser_function': 'detail_parser',
        'column_title': request_payload_config.bdbguaranteecontract_detail_title,
        'table': 'rh_bdbguaranteecontractinfo',  # 原定义的表结构是否有问题？
        'curr_parama_list': ['number'],
        'next_parama_list': ['guaranteecode'],
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
        # 'detail_point': ['rh_guarantor_person_detail', 'rh_guarantor_detail', 'rh_bdbbusinesssum_detail',
        #                  'rh_bdbbusiness_list'],
        'detail_point':['rh_guarantor_person_detail', 'rh_guarantor_detail', 'rh_bdbbusinesssum_detail'],
    },  # 担保信息->被担保信息->保证->自然人保证人信息
    'rh_guarantor_person_detail': {
        'function': 'null_downloader',
        # parser
        'parser_function': 'double_parser',
        'table_selector': 'table[cellspacing="1"] > tr',
        'table_number': 1,
        'tr_select': 5,
        'column_title': request_payload_config.rh_guarantor_person,
        'table': 'rh_guarantor_person',
        'curr_parama_list': ['guaranteecode'],
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },  # 担保信息->被担保信息->保证->保证人信息
    'rh_guarantor_detail': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'double_parser',
        'table_selector': 'table[cellspacing="1"] > tr',
        'table_number': 1,
        'tr_select': 4,
        'column_title': request_payload_config.rh_guarantor,
        'table': 'rh_guarantor',
        'curr_parama_list': ['guaranteecode'],
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    ##被担保合同对应主业务汇总信息
    'rh_bdbbusinesssum_detail': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'list_parser',
        'table_selector': '.tablist',
        # 'table_number': 2,
        # 'table_header': True,
        'column_title': request_payload_config.rh_bdbbusinesssum,
        'table': 'rh_bdbbusinesssum',
        'curr_parama_list': ['guaranteecode'],
        'rename_column_mapping': {'guaranteecode': 'basecode'},
        'next_parama_list':['guaranteecode','businesstype'],
        'detail_point':['rh_bdbbusiness_list'],
        'next_response':True,
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },  # 被担保->保证合同列表信息->该担保合同对应主业务汇总信息->对外担保保证合同详细信息(正则匹配出payload)
    'rh_bdbbusiness_list': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 're_add_post__parser',
        'curr_parama_list': ['guaranteecode','businesstype'],
        'next_parama_list': ['guaranteecode','businesstype'],
        'detail_point': ['rh_bdbbusiness_detail'],
        'next_response':True,
        're_type': True,
        'label_type':'1',
        'loandb_type':'2'
    },
    # 被担保->保证合同列表信息->该担保合同对应主业务汇总信息->对外担保保证合同详细信息
    'rh_bdbbusiness_detail': {
        # downloader
        'function': 'post_downloader',
        'url': 'AssureLoanKindDetailAction.do',
        'column_title': request_payload_config.rh_bdbbusiness,
        'payload': request_payload_config.duiwaidanbaoxinxi_payload,
        'table': 'rh_bdbbusiness',
        # parser
        'parser_function': 'list_parser',
        'curr_parama_list': ['guaranteecode','businesstype'],
        'rename_column_mapping': {'guaranteecode': 'basecode'},
        'table_number': 0,
        'table_header': True,
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    # step3.2.2.2: 被担保抵押合同列表信息
    'securedmort_list': {
        # downloader
        'function': 'post_downloader',
        'url': 'AssureAllActionNew.do',
        'payload': json.loads(
            json.dumps(request_payload_config.bguarantee_list_payload) % '2'),
        # parser
        'parser_function': 'list_parser',
        'table_header': True,
        # next
        'detail_point': ['securedmort_detail'],
    },  # 被担保抵押合同列表信息->抵押合同详细信息
    'securedmort_detail': {
        # downloader
        'function': 'get_downloader',
        # parser
        'parser_function': 'detail_parser',
        'column_title': request_payload_config.rh_bdbmortgagecontract,
        'table': 'rh_bdbmortgagecontract',
        'next_parama_list': ['contractcode'],
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
        'detail_point': ['rh_bdbmortuser_person_detail', 'rh_bdbmortuser_detail',
                         'rh_bdbmortcontractinfo_detail','rh_bdbbusinesssum_detail_1'],
        # 'detail_point':['rh_bdbbusinesssum_detail_1',],
    },  # 被担保自然人抵押人列表信息)
    'rh_bdbmortuser_person_detail': {
        # 暂时没有找到相关有数据的信息
        'function': 'null_downloader',
        # parser
        'parser_function': 'person_parser',
        # 'table_selector': 'table[cellspacing="1"] > tr',
        'special_rows_tr_attrs': {"onclick": "javascript:showDetail('detail0');"},
        'table_number': 1,
        'column_title': request_payload_config.rh_bdbmortuser_person,
        'table': 'rh_bdbmortuser_person',
        'curr_parama_list': ['contractcode'],
        'rename_column_mapping': {'contractcode': 'securedmortcode'},
        'td_length': 5,
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },  # 被担保抵押人列表信息()
    'rh_bdbmortuser_detail': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'person_parser',
        'table_selector': 'table#list',
        'special_rows_tr_attrs': {"onclick": "javascript:showDetail('detail0');"},
        'column_title': request_payload_config.rh_bdbmortuser,
        'table': 'rh_bdbmortuser',
        'curr_parama_list': ['contractcode'],
        'rename_column_mapping': {'contractcode': 'securedmortcode'},
        'td_length': 4,
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
        # 'detail_point':['rh_bdbmortcontractinfo_detail']
    },  # 被担保抵押物信息
    # 'rh_bdbmortcontractinfo_detail':{   #旧版本的被担保信息-》抵押物信息
    #     # downloader
    #     'function': 'null_downloader',
    #     # parser
    #     'parser_function': 'list_parser',
    #     'table_selector': '#detail0 > td > table',
    #     'table_header':True,
    #     'column_title': request_payload_config.rh_bdbmortcontractinfo,
    #     'table': 'rh_bdbmortcontractinfo',
    #     # 'curr_parama_list': ['securedmidsigncode'],
    #     # 'rename_column_mapping':{'securedmidsigncode':'mortmidcode'},
    #     # next
    #     'next_processor': 'saver',
    # },
    'rh_bdbmortcontractinfo_detail': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'goods_parser',
        'table_selector': '#detail0 > td > table',
        'special_rows_tr_attrs': {"onclick": "javascript:showDetail('detail0');"},
        'column_title': request_payload_config.rh_bdbmortcontractinfo,
        'table': 'rh_bdbmortcontractinfo',
        'curr_parama_list': ['contractcode'],
        'rename_column_mapping': {'contractcode': 'mortcontractcode'},
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    'rh_bdbbusinesssum_detail_1': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'list_parser',
        'table_selector': '.tablist',
        'column_title': request_payload_config.rh_bdbbusinesssum,
        'table': 'rh_bdbbusinesssum',
        'curr_parama_list': ['guaranteecode','contractcode'],
        'rename_column_mapping': {'guaranteecode': 'basecode','contractcode': 'basecode'},
        'next_parama_list':['guaranteecode','businesstype','contractcode'],
        'detail_point':['rh_bdbbusiness_list_1'],
        'next_response':True,
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },  # 被担保->保证合同列表信息->该担保合同对应主业务汇总信息->对外担保保证合同详细信息(正则匹配出payload)
    'rh_bdbbusiness_list_1': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 're_add_post__parser',
        'curr_parama_list': ['guaranteecode','businesstype','contractcode'],
        'next_parama_list': ['guaranteecode','businesstype','contractcode'],
        'detail_point': ['rh_bdbbusiness_detail_1'],
        'next_response':True,
        'label_type':'2',
        'loandb_type':'2'
    },
    # 被担保->保证合同列表信息->该担保合同对应主业务汇总信息->对外担保保证合同详细信息
    'rh_bdbbusiness_detail_1': {
        # downloader
        'function': 'post_downloader',
        'url': 'AssureLoanKindDetailAction.do',
        'column_title': request_payload_config.rh_bdbbusiness,
        'payload': request_payload_config.duiwaidanbaoxinxi_payload,
        'table': 'rh_bdbbusiness',
        # parser
        'parser_function': 'list_parser',
        'curr_parama_list': ['guaranteecode','businesstype','contractcode'],
        'rename_column_mapping': {'guaranteecode': 'basecode','contractcode': 'basecode'},
        'table_number': 0,
        'table_header': True,
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    # step3.2.2.3: 被担保质押合同列表信息
    'bdbpledgecontract_list': {
        # downloader
        'function': 'post_downloader',
        'url': 'AssureAllActionNew.do',
        'payload': json.loads(
            json.dumps(request_payload_config.bguarantee_list_payload) % '3'),
        # parser
        'parser_function': 'list_parser',
        'table_header': True,
        # next
        'detail_point': ['bdbpledgecontract_detail'],
    },  # 被担保质押合同列表信息->详细信息
    'bdbpledgecontract_detail': {
        # downloader
        'function': 'get_downloader',
        # parser
        'parser_function': 'detail_parser',
        'column_title': request_payload_config.rh_bdbpledgecontract,
        'table': 'rh_bdbpledgecontract',
        'next_parama_list': ['contractcode'],
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
        'detail_point': ['rh_bdbpledgemome_person_detail', 'rh_bdbpledgemome_detail',
                         'rh_bdbpledgemomelist_detail','rh_bdbbusinesssum_detail_2'],
        # 'detail_point':['rh_bdbbusinesssum_detail_2'],
    },  # 被担保自然人质押人信息
    'rh_bdbpledgemome_person_detail': {
        # 暂时没有找到相关有数据的信息
        'function': 'null_downloader',
        # parser
        'parser_function': 'person_parser',
        'table_selector': 'table#list',
        # 'table_selector': 'table[cellspacing="1"] > tr',
        'special_rows_tr_attrs': {"onclick": "javascript:showDetail('detail0');"},
        'table_number': 1,
        'column_title': request_payload_config.rh_bdbpledgemome_person,
        'table': 'rh_bdbpledgemome_person',
        'td_length': 5,
        'curr_parama_list': ['contractcode'],
        'rename_column_mapping': {'contractcode': 'pledgecode'},
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },  # 被担保质押人信息
    'rh_bdbpledgemome_detail': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'person_parser',
        'table_selector': 'table#list',
        'special_rows_tr_attrs': {"onclick": "javascript:showDetail('detail0');"},
        'column_title': request_payload_config.rh_bdbpledgemome,
        'table': 'rh_bdbpledgemome',
        'td_length': 4,
        'curr_parama_list': ['contractcode'],
        'rename_column_mapping': {'contractcode': 'pledgecode'},
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },  # 质押物信息(rh_bdbpledgemomelist)
    # 'rh_bdbpledgemomelist_detail':{  #旧版本的被担保信息->质押物信息
    #     # downloader
    #     'function': 'null_downloader',
    #     # parser
    #     'parser_function': 'list_parser',
    #     'table_selector': '#detail0 > td > table',
    #     'table_header':True,
    #     'column_title': request_payload_config.rh_bdbpledgemomelist,
    #     'table': 'rh_bdbpledgemomelist',
    #     # next
    #     'next_processor': 'saver',
    # },
    'rh_bdbpledgemomelist_detail': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'goods_parser',
        'table_selector': '#detail0 > td > table',
        'special_rows_tr_attrs': {"onclick": "javascript:showDetail('detail0');"},
        'column_title': request_payload_config.rh_bdbpledgemomelist,
        'table': 'rh_bdbpledgemomelist',
        'curr_parama_list': ['contractcode'],
        'rename_column_mapping': {'contractcode': 'pledgecode'},
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },#该担保合同对应主业务汇总信息
    'rh_bdbbusinesssum_detail_2': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'list_parser',
        'table_selector': '.tablist',
        'column_title': request_payload_config.rh_bdbbusinesssum,
        'table': 'rh_bdbbusinesssum',
        'curr_parama_list': ['contractcode'],
        'rename_column_mapping': {'contractcode': 'basecode'},
        'next_parama_list':['businesstype','contractcode'],
        'detail_point':['rh_bdbbusiness_list_2'],
        'next_response':True,
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    }, #该担保合同对应主业务汇总信息->对外担保保证合同详细信息(正则匹配出payload)
    'rh_bdbbusiness_list_2': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 're_add_post__parser',
        'curr_parama_list': ['businesstype','contractcode'],
        'next_parama_list': ['businesstype','contractcode'],
        'detail_point': ['rh_bdbbusiness_detail_2'],
        'next_response':True,
        'label_type':'3',
        'loandb_type':'2'
    },
    # 该担保合同对应主业务汇总信息->对外担保保证合同详细信息
    'rh_bdbbusiness_detail_2': {
        # downloader
        'function': 'post_downloader',
        'url': 'AssureLoanKindDetailAction.do',
        'column_title': request_payload_config.rh_bdbbusiness,
        'payload': request_payload_config.duiwaidanbaoxinxi_payload,
        'table': 'rh_bdbbusiness',
        # parser
        'parser_function': 'list_parser',
        'curr_parama_list': ['businesstype','contractcode'],
        'rename_column_mapping': {'contractcode': 'basecode'},
        'table_number': 0,
        'table_header': True,
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    # step3.3: 欠息信息
    'interestinfosum_before_list': {
        # downloader
        'function': 'post_downloader',
        'url': 'OweListActionBefore.do',
        'payload': request_payload_config.interestinfo_before_payload,
        # parser
        'parser_function': 'null_parser',
        # next
        'detail_point': ['interestinfosum_list'],
    },
    'interestinfosum_list': {
        # downloader
        'function': 'post_downloader',
        'url': 'OweListAction.do',
        'payload': request_payload_config.interestinfo_list_payload,
        # parser
        'parser_function': 'list_parser',
        'table_header': True,
        # next
        'detail_point': ['interestinfo_list'],
    },
    # step3.3.1:欠息 表内 + 表外
    'interestinfo_list': {
        # downloader
        'function': 'get_downloader',
        # parser
        'parser_function': 'list_parser',
        'table_header': True,
        # next
        'detail_point': ['interestinfo_detail'],
    },
    'interestinfo_detail': {
        # downloader
        'function': 'get_downloader',
        'column_title': request_payload_config.interestinfo_detail_title,
        'table': 'rh_interestinfo',
        # parser
        'parser_function': 'detail_parser',
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    # step3.4: 公开授信
    'creditagreeement_list': {
        # downloader
        'function': 'get_downloader',
        'url': 'creditinfosearch.do',
        'payload': request_payload_config.creditagreeement_list_payload,
        'table_selector': 'table#list > tbody > tr',
        'table_header': True,
        # parser
        'parser_function': 'list_parser',
        # next
        'detail_point': ['creditagreeement_detail'],
    },
    'creditagreeement_detail': {
        # downloader
        'function': 'get_downloader',
        'column_title': request_payload_config.creditagreeement_detail_title,
        'table': 'rh_creditagreement',
        # parser
        'parser_function': 'detail_parser',
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    # step3.5: 垫款信息
    'martpad_before_list': {
        # downloader
        'function': 'post_downloader',
        'url': 'PkListActionBefore.do',
        'payload': request_payload_config.martpad_before_list_payload,
        # parser
        'parser_function': 'null_parser',
        # next
        'detail_point': ['martpad_list'],
    },
    'martpad_list': {
        # downloader
        'function': 'post_downloader',
        'url': 'PkListAction.do',
        'payload': request_payload_config.martpad_list_payload,
        'table_header': True,
        'table_footer': True,
        # parser
        'parser_function': 'list_parser',
        # next
        'detail_point': ['martpad_detail'],
    },
    'martpad_detail': {
        # downloader
        'function': 'get_downloader',
        'column_title': request_payload_config.martpad_detail_title,
        'table': 'rh_martpad',
        # parser
        'parser_function': 'detail_parser',
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    'baddebtinfo_before_list': {
        # 4不良负债信息download//20161027号添加
        'function': 'post_downloader',
        'url': 'HadowesAction.do',
        'payload': request_payload_config.baddebtinfo_list_payload,
        'column_title': request_payload_config.rh_baddebtinfo,
        'table': 'rh_baddebtinfo',
        'ignore_detail_urls': True,
        # parser
        'parser_function': 'list_parser',
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
        ###################################################################################################################################
        # baddebinfo_detail 贷款余额
        # baddebinfo_baoli_before  保理余额
        # baddebinfo_rongzhixieyi_before 贸易融资余额
        # baddebinfo_piaojutiexian_before  票据贴现（未结清金额）
        # baddebinfo_xinyongzheng_before  信用证余额
        # baddebinfo_daikuanyue_before   类贷款余额
        # baddebinfo_chengdui_before   承兑汇票（未结清金额）
        # baddebinfo_baohan_before   保函余额
        #################################################################################################################################
        'detail_point': ['baddebinfo_detail', 'baddebinfo_baoli_before', 'baddebinfo_rongzhixieyi_before',
                         'baddebinfo_piaojutiexian_before',
                         'baddebinfo_xinyongzheng_before', 'baddebinfo_daikuanyue_before', 'baddebinfo_chengdui_before',
                         'baddebinfo_baohan_before'],
        # 'detail_point':['baddebinfo_detail'],
    },
    # 4.1不良负债信息->贷款余额
    'baddebinfo_detail': {
        'function': 'post_downloader',
        'url': 'HadowesDetailAction.do',
        'column_title': request_payload_config.rh_loaninfo_d_before,
        'payload': json.loads(json.dumps(request_payload_config.baddebtinfo_balance_payload) % '1'),
        'next_parama_list': ['balancecurrency', 'balanceloan'],
        'parser_function': 'list_parser',
        'table_header': True,
        'detail_point': ['baddebinfo_detail_parser']
    },
    # 4.1.1不良负债信息->贷款合同详细信息
    'baddebinfo_detail_parser': {
        # downloader
        'function': 'get_downloader',
        # parser
        'parser_function': 'detail_parser',
        'column_title': request_payload_config.rh_loaninfo_d,
        'table': 'rh_loaninfo_d',
        'curr_parama_list': ['balancecurrency', 'balanceloan'],
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    ##4.2不良负债信息-> '保理余额 '
    'baddebinfo_baoli_before': {
        'function': 'post_downloader',
        'url': 'HadowesDetailAction.do',
        'payload': json.loads(json.dumps(request_payload_config.baddebtinfo_balance_payload) % '2'),
        'parser_function': 'list_parser',
        'table_header': True,
        'table_footer': True,
        'detail_point': ['baddebinfo_baoli_list']
    },
    ##4.2.1不良负债信息-> ,'不良负债保理详细信息'
    'baddebinfo_baoli_list': {
        'function': 'get_downloader',
        'parser_function': 'detail_parser',
        'column_title': request_payload_config.rh_factoringinfo_d,
        'table': 'rh_factoringinfo_d',
        'table_selector': 'table#list > tr > td',
        # 'table_footer':True,
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    # 4.3不良负债信息->贸易融资余额
    'baddebinfo_rongzhixieyi_before': {
        'function': 'post_downloader',
        'url': 'HadowesDetailAction.do',
        'payload': json.loads(json.dumps(request_payload_config.baddebtinfo_balance_payload) % '3'),
        'parser_function': 'list_parser',
        'table_header': True,
        'detail_point': ['baddebinfo_rongzhixieyi_list']
    },
    # 4.3.1不良负债信息->不良负债融资协议信息-->
    'baddebinfo_rongzhixieyi_list': {
        # downloader
        'function': 'get_downloader',
        # parser
        'parser_function': 'detail_parser',
        'column_title': request_payload_config.rh_fagreementinfo_d,
        'table': 'rh_fagreementinfo_d',
        # 'table_footer':True,
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    ##4.4不良负债信息->'票据贴现（未结清金额） '
    'baddebinfo_piaojutiexian_before': {
        'function': 'post_downloader',
        'url': 'HadowesDetailAction.do',
        'payload': json.loads(json.dumps(request_payload_config.baddebtinfo_balance_payload) % '4'),
        'parser_function': 'list_parser',
        'table_header': True,
        'detail_point': ['baddebinfo_piaojutiexian_list']
    },
    ##4.4.1不良负债信息->票据贴现（未结清金额）->不良负债借款人票据贴现详细信息
    'baddebinfo_piaojutiexian_list': {
        # downloader
        'function': 'get_downloader',
        # parser
        'parser_function': 'detail_parser',
        'column_title': request_payload_config.rh_billdiscount_d,
        'table': 'rh_billdiscount_d',
        # 'table_footer':True,
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    ##4.5不良负债信息-> '信用证余额 '
    'baddebinfo_xinyongzheng_before': {
        'function': 'post_downloader',
        'url': 'HadowesDetailAction.do',
        'payload': json.loads(json.dumps(request_payload_config.baddebtinfo_balance_payload) % '6'),
        'parser_function': 'list_parser',
        'table_header': True,
        'detail_point': ['baddebinfo_xinyongzheng_list']
    },
    ##4.5.1不良负债信息-> '不良负债借款人信用证详细信息'
    'baddebinfo_xinyongzheng_list': {
        # downloader
        'function': 'get_downloader',
        # parser
        'parser_function': 'detail_parser',
        'column_title': request_payload_config.rh_creditbalance_d,
        'table': 'rh_creditbalance_d',
        # 'table_footer':True,
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    ##4.6不良负债信息-> ,'类贷款余额 '
    'baddebinfo_daikuanyue_before': {
        'function': 'post_downloader',
        'url': 'HadowesDetailAction.do',
        'payload': json.loads(json.dumps(request_payload_config.baddebtinfo_balance_payload) % '9'),
        'parser_function': 'list_parser',
        'table_header': True,
        'detail_point': ['baddebinfo_daikuanyue_list']
    },
    ##4.6.1不良负债信息-> ,'不良负债类贷款余额合约信息'
    'baddebinfo_daikuanyue_list': {
        # downloader
        'function': 'get_downloader',
        # parser
        'parser_function': 'detail_parser',
        'column_title': request_payload_config.rh_specialloaninfo_d,
        'table': 'rh_specialloaninfo_d',
        # 'table_footer':True,
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    ##4.7不良负债信息-> ,'承兑汇票（未结清金额） '
    'baddebinfo_chengdui_before': {
        'function': 'post_downloader',
        'url': 'HadowesDetailAction.do',
        'payload': json.loads(json.dumps(request_payload_config.baddebtinfo_balance_payload) % '5'),
        'parser_function': 'list_parser',
        'table_header': True,
        'detail_point': ['baddebinfo_chengdui_list']
    },
    # 4.7.1不良负债信息-> ,'不良负债借款人承兑汇票详细信息'
    'baddebinfo_chengdui_list': {
        # downloader
        'function': 'get_downloader',
        # parser
        'parser_function': 'detail_parser',
        'column_title': request_payload_config.rh_draft_d,
        'table': 'rh_draft_d',
        # 'table_footer':True,
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    ##4.8不良负债信息-> 保函余额
    'baddebinfo_baohan_before': {
        'function': 'post_downloader',
        'url': 'HadowesDetailAction.do',
        'payload': json.loads(json.dumps(request_payload_config.baddebtinfo_balance_payload) % '7'),
        'parser_function': 'list_parser',
        'table_header': True,
        'detail_point': ['baddebinfo_baohan_list']
    },
    # 4.8.1不良负债信息-> 不良负债借款人保函详细信息
    'baddebinfo_baohan_list': {
        # downloader
        'function': 'get_downloader',
        # parser
        'parser_function': 'detail_parser',
        'column_title': request_payload_config.rh_guaranteeha_d,
        'table': 'rh_guaranteeha_d',
        'table_footer': True,
        # next
        'next_processor': 'saver',
        'add_searchdate': True,
    },
    # 发生额信息5.0 start
    'rh_fashenge_befor_list': {
        'function': 'post_downloader',
        'url': 'OweOccurQueryAction.do',
        'payload': request_payload_config.rh_fashenge_payload,
        'column_title': request_payload_config.rh_balancetypesum_f,
        'table': 'rh_balancetypesum_f',
        'ignore_detail_urls': True,
        # parser
        'parser_function': 'list_parser',
        'curr_parama_list': ['starttime', 'endtime'],
        # next
        'next_processor': 'saver',
        'date_range': ['starttime', 'endtime'],
        ###########################################################################################
        # rh_fashenge_daikuan_list  贷款发生额
        # rh_fashenge_leidaikuan_list  类贷款发生额  没有找到数据
        # rh_fashenge_baoli_list   保理发生额
        # rh_fashenge_maoyirongzhi_list  贸易融资发生额
        # rh_fashenge_piaojutixian_list  票据贴现发生额
        # rh_fashenge_chengduihuipiao_list  承兑汇票发生额
        # rh_fashenge_xinyongzheng_list  信用证发生额
        # rh_fashenge_baohan_list  保函发生额
        'detail_point': ['rh_fashenge_daikuan_list', 'rh_fashenge_baoli_list', 'rh_fashenge_maoyirongzhi_list',
                         'rh_fashenge_piaojutixian_list', 'rh_fashenge_chengduihuipiao_list',
                         'rh_fashenge_xinyongzheng_list', 'rh_fashenge_baohan_list'],
        # 这里需要加入需要分别爬取的发生额信息分支（共9个）
        # 'detail_point':['rh_fashenge_daikuan_list'],
    },
    # 发生额信息5.1.1->贷款发生额
    'rh_fashenge_daikuan_list': {
        'function': 'post_downloader',
        'url': 'OweOccurDetailAction.do',
        'payload': json.loads(json.dumps(request_payload_config.rh_fashenge_below_payload) % '1'),
        # parser
        'parser_function': 'list_parser',
        'table_header': True,
        'table_footer': True,
        # next
        'detail_point': ['rh_fashenge_daikuan_detail'],
    },
    # 发生额信息5.1.1->贷款发生额->贷款合同信息
    'rh_fashenge_daikuan_detail': {
        # downloader
        'function': 'get_downloader',
        # parser
        'parser_function': 'detail_parser',
        'column_title': request_payload_config.rh_loaninfo_f,
        'table': 'rh_loaninfo_f',
        'curr_parama_list': ['balanceloan'],
        'next_parama_list': ['contractnumber'],
        # next
        # rh_fashenge_hetong_baozheng_list 保证合同信息
        # rh_fashenge_hetong_jieju_detail  借据信息
        # rh_fashenge_hetong_diya_detail   抵押合同信息
        # rh_fashenge_hetong_zhiya_detail  质押合同信息
        'detail_point': ['rh_fashenge_hetong_baozheng_list', 'rh_fashenge_hetong_jieju_detail',
                         'rh_fashenge_hetong_diya_detail', 'rh_fashenge_hetong_zhiya_detail'],
        # 'detail_point':['rh_fashenge_hetong_diya_detail'], #
        'next_processor': 'saver',
        'date_range': ['starttime', 'endtime'],
    },
    'rh_fashenge_hetong_baozheng_list': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'list_parser',
        'table_footer': True,
        'table_number': 2,
        'table_selector': 'table[cellspacing="1"]',
        'curr_parama_list': ['contractnumber', 'factoringcode', 'draftagreementcode', 'creditcode', 'guaranteecode','financecode'],
        'next_parama_list': ['contractnumber', 'factoringcode', 'draftagreementcode', 'creditcode', 'guaranteecode','financecode'],
        # next
        'detail_point': ['rh_fashenge_hetong_baozheng_detail'],
    },
    # 发生额信息5.1.2.1->贷款发生额->贷款合同信息->保证合同信息->保证合同概要信息
    'rh_fashenge_hetong_baozheng_detail': {
        # downloader
        'function': 'get_downloader',
        # parser
        'parser_function': 'detail_parser',
        'column_title': request_payload_config.rh_guaranteecontractinfo_f,
        'table': 'rh_guaranteecontractinfo_f',
        'curr_parama_list': ['contractnumber','factoringcode', 'draftagreementcode', 'creditcode', 'guaranteecode','financecode'],
        'next_parama_list': ['contractencoding'],
        'rename_column_mapping': {'factoringcode': 'contractnumber', 'draftagreementcode': 'contractnumber',
                                  'creditcode': 'contractnumber', 'guaranteecode': 'contractnumber','financecode':'contractnumber'},
        # next
        'detail_point': ['rh_fashenge_hetong_ziranrenbaozhengren_detail', 'rh_fashenge_hetong_baozhengren_detail'],
        'next_processor': 'saver',
        'date_range': ['starttime', 'endtime'],
    },
    # 发生额信息5.1.2.1->贷款发生额->贷款合同信息->保证合同信息->自然人保证人信息
    'rh_fashenge_hetong_ziranrenbaozhengren_detail': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'list_parser',
        'column_title': request_payload_config.rh_guaranteinfo_person_f,
        'table': 'rh_guaranteinfo_person_f',
        'table_number': 2,
        'tr_select': 5,
        'curr_parama_list': ['contractencoding'],
        # next
        'next_processor': 'saver',
        'date_range': ['starttime', 'endtime'],
    },
    # 发生额信息5.1.2.1->贷款发生额->贷款合同信息->保证合同信息->保证人信息
    'rh_fashenge_hetong_baozhengren_detail': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'list_parser',
        'column_title': request_payload_config.rh_guaranteinfo_f,
        'table': 'rh_guaranteinfo_f',
        'table_header': True,
        'table_number': 3,
        'tr_select': 4,
        'table_selector': 'table[align="center"]',
        'curr_parama_list': ['contractencoding'],
        # next
        'next_processor': 'saver',
        'date_range': ['starttime', 'endtime'],
    },

    # 发生额信息5.1.3->贷款发生额->贷款合同信息->抵押合同信息
    'rh_fashenge_hetong_diya_detail': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'list_parser',
        'table_number': 3,
        'table_selector': 'table[cellspacing="1"]',
        'curr_parama_list': ['contractnumber', 'factoringcode', 'draftagreementcode', 'creditcode', 'guaranteecode','financecode'],
        'next_parama_list': ['contractnumber', 'factoringcode', 'draftagreementcode', 'creditcode', 'guaranteecode','financecode'],
        # next
        'detail_point': ['rh_fashenge_hetong_diyagaiyao_detail'],
    },
    # 发生额信息5.1.3->贷款发生额->贷款合同信息->抵押合同信息->抵押合同概要信息
    'rh_fashenge_hetong_diyagaiyao_detail': {
        # downloader
        'function': 'get_downloader',
        # parser
        'parser_function': 'detail_parser',
        'column_title': request_payload_config.rh_mortgagecontract_f,
        'table': 'rh_mortgagecontract_f',
        # 贷款余额，保理余额
        'curr_parama_list': ['contractnumber', 'factoringcode', 'draftagreementcode', 'creditcode', 'guaranteecode','financecode'],
        'next_parama_list': ['mortcontractcode'],
        'rename_column_mapping': {'factoringcode': 'contractnumber', 'draftagreementcode': 'contractnumber',
                                  'creditcode': 'contractnumber', 'guaranteecode': 'contractnumber','financecode':'contractnumber'},
        'date_range': ['starttime', 'endtime'],
        # next
        'detail_point': ['rh_fashenge_hetong_zirandiyagaiyao_detail', 'rh_fashenge_hetong_diyaren_detail',
                         'rh_fashenge_hetong_diyawu_detail'],
        # 'detail_point': [ 'rh_fashenge_hetong_zirandiyagaiyao_detail'],
        'next_processor': 'saver',
    },
    # 发生额信息5.1.3.1->贷款发生额->贷款合同信息->抵押合同信息->抵押合同概要信息->发生额自然人抵押人信息(rh_mortgageinfo_person_f)
    'rh_fashenge_hetong_zirandiyagaiyao_detail': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'person_parser',
        # 'table_header': True,
        # 'special_rows_tr_attrs': {'onclick': '', 'id': ''},
        'special_rows_tr_attrs': {"onclick": "javascript:showDetail('detail0');"},
        'column_title': request_payload_config.rh_mortgageinfo_person_f,
        'table': 'rh_mortgageinfo_person_f',
        'table_number': 1,
        'td_length': 5,
        'curr_parama_list': ['mortcontractcode'],
        # next
        'next_processor': 'saver',
        'date_range': ['starttime', 'endtime'],
    },
    # 发生额信息5.1.3.2->贷款发生额->贷款合同信息->抵押合同信息->抵押合同概要信息->发生额抵押人信息(rh_mortgageinfo_f)
    'rh_fashenge_hetong_diyaren_detail': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'person_parser',
        'special_rows_tr_attrs': {"onclick": "javascript:showDetail('detail0');"},
        'column_title': request_payload_config.rh_mortgageinfo_f,
        'table': 'rh_mortgageinfo_f',
        'table_number': 1,
        'td_length': 4,
        'curr_parama_list': ['mortcontractcode'],
        # next
        'next_processor': 'saver',
        'date_range': ['starttime', 'endtime'],
    },
    # 发生额信息5.1.3.3->贷款发生额->贷款合同信息->抵押合同信息->抵押合同概要信息->发生额抵押物信息(rh_mortcontractinfo_f)
    # 'rh_fashenge_hetong_diyawu_detail': {   #旧版本的发生额抵押物解析函数
    #     # downloader
    #     'function': 'null_downloader',
    #     # parser
    #     'parser_function': 'list_parser',
    #     'table_number': 2,
    #     'table_selector': 'table[cellspacing="1"]',
    #     'column_title': request_payload_config.rh_mortcontractinfo_f,
    #     'table': 'rh_mortcontractinfo_f',
    #     'curr_parama_list': ['mortcontractcode'],
    #     # next
    #     'next_processor': 'saver',
    #     'date_range':['starttime','endtime'],
    # },
    'rh_fashenge_hetong_diyawu_detail': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'goods_parser',
        'table_selector': '#detail0 > td > table',
        'special_rows_tr_attrs': {"onclick": "javascript:showDetail('detail0');"},
        'column_title': request_payload_config.rh_mortcontractinfo_f,
        'table': 'rh_mortcontractinfo_f',
        'curr_parama_list': ['mortcontractcode'],
        # next
        'next_processor': 'saver',
        'date_range': ['starttime', 'endtime'],
    },
    # 发生额信息5.1.4->贷款发生额->贷款合同信息->质押合同信息
    'rh_fashenge_hetong_zhiya_detail': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'list_parser',
        'table_footer': True,
        'table_number': 4,
        'table_selector': 'table[cellspacing="1"]',
        'curr_parama_list': ['contractnumber', 'factoringcode', 'draftagreementcode', 'creditcode', 'guaranteecode','financecode'],
        'next_parama_list': ['contractnumber', 'factoringcode', 'draftagreementcode', 'creditcode', 'guaranteecode','financecode'],
        # next
        'detail_point': ['rh_fashenge_hetong_zhiyahetong_detail'],
    },
    # 发生额信息5.1.4.1->贷款发生额->贷款合同信息->质押合同概要信息
    'rh_fashenge_hetong_zhiyahetong_detail': {
        # downloader
        'function': 'get_downloader',
        # parser
        'parser_function': 'detail_parser',
        'column_title': request_payload_config.rh_borrowerpledgeinfo_f,
        'table': 'rh_borrowerpledgeinfo_f',
        'curr_parama_list': ['contractnumber','factoringcode', 'draftagreementcode', 'creditcode', 'guaranteecode','financecode'],
        'next_parama_list': ['pledgecode'],
        'rename_column_mapping': {'factoringcode': 'contractnumber', 'draftagreementcode': 'contractnumber',
                                  'creditcode': 'contractnumber', 'guaranteecode': 'contractnumber','financecode':'contractnumber'},
        # next
        'next_processor': 'saver',
        'date_range': ['starttime', 'endtime'],
        'detail_point': ['rh_fashenge_hetong_zhiyaren_detail', 'rh_fashenge_hetong_ziranzhiyaren_detail',
                         'rh_fashenge_hetong_zhiyawu_detail'],
    },
    # 发生额信息5.1.4.1.1->贷款发生额->贷款合同信息->质押合同概要信息->发生额质押人信息(rh_pledgemome_f)
    'rh_fashenge_hetong_zhiyaren_detail': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'person_parser',
        'special_rows_tr_attrs': {"onclick": "javascript:showDetail('detail0');"},
        'column_title': request_payload_config.rh_pledgemome_f,
        'table': 'rh_pledgemome_f',
        'curr_parama_list': ['pledgecode'],
        'table_number': 1,
        'td_length': 4,
        # next
        'next_processor': 'saver',
        'date_range': ['starttime', 'endtime'],
    },
    # 发生额信息5.1.4.1.2->贷款发生额->贷款合同信息->质押合同概要信息->发生额自然人质押人信息(rh_pledgemome_person_f)
    'rh_fashenge_hetong_ziranzhiyaren_detail': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'person_parser',
        # 'special_rows_tr_attrs': {'onclick': '', 'id': ''},
        'special_rows_tr_attrs': {"onclick": "javascript:showDetail('detail0');"},
        'column_title': request_payload_config.rh_pledgemome_person_f,
        'table': 'rh_pledgemome_person_f',
        'curr_parama_list': ['pledgecode'],
        # 'table_header': True,
        'table_number': 1,
        'td_length': 5,
        # next
        'next_processor': 'saver',
        'date_range': ['starttime', 'endtime'],
    },
    # 发生额信息5.1.4.1.3->贷款发生额->贷款合同信息->质押合同概要信息->发生额质押物信息(rh_pledgemomelist_f)
    # 'rh_fashenge_hetong_zhiyawu_detail':{    #旧版本的质押物解析配置
    #     # downloader
    #     'function': 'null_downloader',
    #     # parser
    #     'parser_function': 'list_parser',
    #     'table_selector': 'table[cellspacing="1"]',
    #     'column_title': request_payload_config.rh_pledgemomelist_f,
    #     'table': 'rh_pledgemomelist_f',
    #     'table_number':2,
    #     # next
    #     'next_processor': 'saver',
    #     'date_range':['starttime','endtime'],
    # },
    'rh_fashenge_hetong_zhiyawu_detail': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'goods_parser',
        'table_selector': '#detail0 > td > table',
        'special_rows_tr_attrs': {"onclick": "javascript:showDetail('detail0');"},
        'column_title': request_payload_config.rh_pledgemomelist_f,
        'table': 'rh_pledgemomelist_f',
        'curr_parama_list': ['pledgecode'],
        # next
        'next_processor': 'saver',
        'date_range': ['starttime', 'endtime'],
    },
    # 发生额信息5.1.5->贷款发生额->贷款合同信息->借据信息
    'rh_fashenge_hetong_jieju_detail': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'list_parser',
        'column_title': request_payload_config.iouinfo_list_title,
        'curr_parama_list': ['contractnumber'],
        'next_parama_list': ['contractnumber', 'businessdate'],
        'table_number': -1,
        # next
        'detail_point': ['rh_fashenge_hetong_jiejuxinxi_detail']
    },
    # 发生额信息5.1.5.1->贷款发生额->贷款合同信息->借据信息 -->借据信息
    'rh_fashenge_hetong_jiejuxinxi_detail': {
        # downloader
        'function': 'get_downloader',
        # parser
        'parser_function': 'detail_parser',
        'column_title': request_payload_config.rh_iouinfo_f,
        'table': 'rh_iouinfo_f',
        'curr_parama_list': ['contractnumber', 'businessdate'],
        'next_parama_list': ['ioucode'],
        # next
        'next_processor': 'saver',
        'date_range': ['starttime', 'endtime'],
        'detail_point': ['rh_fashenge_hetong_huankuan_detail', 'rh_fashenge_hetong_zhanqixinxi_detail'],
    },
    # 发生额信息5.1.5.1.1->贷款发生额->贷款合同信息->借据信息 -->发生额还款信息(rh_repaymentinfo_f)*
    'rh_fashenge_hetong_huankuan_detail': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'mix_list_parser',
        'column_title': request_payload_config.rh_repaymentinfo_f,
        'table': 'rh_repaymentinfo_f',
        'table_number': 1,
        'curr_parama_list': ['ioucode'],
        # next
        'next_processor': 'saver',
        'date_range': ['starttime', 'endtime'],
    },
    # 发生额信息5.1.5.1.2->贷款发生额->贷款合同信息->借据信息 -->发生额展期信息/延期信息(rh_extensioninfo_f)
    'rh_fashenge_hetong_zhanqixinxi_detail': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'mix_list_parser',
        'column_title': request_payload_config.rh_extensioninfo_f,
        'table': 'rh_extensioninfo_f',
        'table_number': 2,
        'curr_parama_list': ['ioucode'],
        # next
        'next_processor': 'saver',
        'date_range': ['starttime', 'endtime'],
    },
    #     #发生额信息5.2.0->类贷款发生额
    ##TODO    #发生额信息5.2.1->类贷款发生额->暂时在页面上没找到相关信息
    #     'rh_fashenge_leidaikuan_list':{
    #         'function':'post_downloader',
    #         'url':'OweOccurDetailAction.do',
    #         'payload':json.loads(json.dumps(request_payload_config.rh_fashenge_below_payload)%'9'),
    #         #parser
    #         'parser_function': 'list_parser',
    #         'table_header':True,
    #         #next
    #         'detail_point': ['rh_fashenge_leidaikuan_detail'],
    #     },
    #  #发生额信息5.2.1->类贷款发生额->????????????   '遗留'？？？？？？？？？？？？？？三级页面解析
    #     'rh_fashenge_leidaikuan_detail':{
    #         # downloader
    #         'function': 'get_downloader',
    #         # parser
    #         'parser_function': 'detail_parser',
    #         'column_title': request_payload_config.rh_specialloaninfo_f,
    #         'table': 'rh_specialloaninfo_f',
    #         'table_footer':True,
    #         'table_number':0,
    #         # next
    #         'next_processor': 'saver',
    #     },
    # 发生额信息5.3.0->保理发生额
    'rh_fashenge_baoli_list': {
        'function': 'post_downloader',
        'url': 'OweOccurDetailAction.do',
        'payload': json.loads(json.dumps(request_payload_config.rh_fashenge_below_payload) % '2'),
        # parser
        'parser_function': 'list_parser',
        'table_header': True,
        'table_footer': True,
        # next
        # rh_fashenge_maoyirongzhi_detail  贸易融资发生额->融资协议信息
        'detail_point': ['rh_fashenge_baoli_detail'],
    },
    # 发生额信息5.3.1->保理发生额->保理信息
    'rh_fashenge_baoli_detail': {
        # downloader
        'function': 'get_downloader',
        # parser
        'parser_function': 'detail_parser',
        'table_selector': '.tbcolor > tr:nth-of-type(2) > td:nth-of-type(1) tr > td',
        'column_title': request_payload_config.rh_factoringinfo_f,
        'table': 'rh_factoringinfo_f',
        # next
        'next_processor': 'saver',
        'date_range': ['starttime', 'endtime'],
        'next_parama_list':['factoringcode'],
        'detail_point': ['rh_fashenge_hetong_baozheng_list', 'rh_fashenge_hetong_diya_detail',
                         'rh_fashenge_hetong_zhiya_detail'],
        # 'detail_point':['rh_fashenge_hetong_baozheng_list'],
    },
    # 发生额信息5.4.0->贸易融资发生额
    'rh_fashenge_maoyirongzhi_list': {
        'function': 'post_downloader',
        'url': 'OweOccurDetailAction.do',
        'payload': json.loads(json.dumps(request_payload_config.rh_fashenge_below_payload) % '3'),
        # parser
        'parser_function': 'list_parser',
        'table_header': True,
        'table_footer': True,
        'next_parama_list': ['financeingbalance'],
        # next
        # rh_fashenge_maoyirongzhi_detail  贸易融资发生额->融资协议信息
        'detail_point': ['rh_fashenge_maoyirongzhixinxi_detail'],
    },
    # 发生额信息5.4.1.1->贸易融资发生额->融资协议信息
    'rh_fashenge_maoyirongzhixinxi_detail': {
        # downloader
        'function': 'get_downloader',
        # parser
        'parser_function': 'detail_parser',
        'column_title': request_payload_config.rh_fagreementinfo_f,
        'table': 'rh_fagreementinfo_f',
        'curr_parama_list': ['financeingbalance'],
        'next_parama_list': ['financecode'],
        'detail_point': ['rh_fashenge_rongzhiyewu_detail'],
        'next_processor': 'saver',
        'date_range': ['starttime', 'endtime'],
    },
    # 发生额信息5.4.1.2->贸易融资发生额->融资业务信息
    'rh_fashenge_rongzhiyewu_detail': {
        # downloader
        'function': 'null_downloader',
        # parser
        'parser_function': 'list_parser',
        'table_number': -1,
        'column_title': request_payload_config.rh_financebusiness_f_before,
        'curr_parama_list': ['financecode'],
        'next_parama_list': ['financecode', 'businessdate'],
        'detail_point': ['rh_fashenge_rongzhiyewuxinxi_detail'],
    },
    ##发生额信息5.4.1.2.1->贸易融资发生额->融资业务信息->发生额融资业务信息(rh_financebusiness_f)
    'rh_fashenge_rongzhiyewuxinxi_detail': {
        # downloader
        'function': 'get_downloader',
        # parser
        'parser_function': 'detail_parser',
        'column_title': request_payload_config.rh_financebusiness_f,
        'table': 'rh_financebusiness_f',
        'curr_parama_list': ['financecode', 'businessdate'],
        'next_parama_list': ['financebussinesscode'],
        'table_footer': True,
        # 'detail_point': [],表中没有找到下面的还款和展期表
        'next_processor': 'saver',
        'date_range': ['starttime', 'endtime'],
    },
    # 发生额信息5.5.0->票据贴现发生额
    'rh_fashenge_piaojutixian_list': {
        'function': 'post_downloader',
        'url': 'OweOccurDetailAction.do',
        'payload': json.loads(json.dumps(request_payload_config.rh_fashenge_below_payload) % '4'),
        # parser
        'parser_function': 'list_parser',
        'table_header': True,
        'table_footer': True,
        # next
        # rh_fashenge_piaojutixian_detail  票据贴现发生额->借款人票据贴现详细信息
        'detail_point': ['rh_fashenge_piaojutixian_detail'],
    },
    # 发生额信息5.5.1->票据贴现发生额->借款人票据贴现详细信息
    'rh_fashenge_piaojutixian_detail': {
        # downloader
        'function': 'get_downloader',
        # parser
        'parser_function': 'detail_parser',
        'column_title': request_payload_config.rh_billdiscount_f,
        'table': 'rh_billdiscount_f',
        # next
        'next_processor': 'saver',
        'date_range': ['starttime', 'endtime'],
    },
    # 发生额信息5.6.0->承兑汇票发生额
    'rh_fashenge_chengduihuipiao_list': {
        'function': 'post_downloader',
        'url': 'OweOccurDetailAction.do',
        'payload': json.loads(json.dumps(request_payload_config.rh_fashenge_below_payload) % '5'),
        'column_title': request_payload_config.rh_draft_befor,
        'next_parama_list': ['acceptancedate'],
        # parser
        'parser_function': 'list_parser',
        'table_header': True,
        'table_footer': True,
        # next
        # rh_fashenge_piaojutixian_detail  票据贴现发生额->借款人票据贴现详细信息
        'detail_point': ['rh_fashenge_chengduihuipiao_detail'],
    },
    # 发生额信息5.6.1->承兑汇票发生额->借款人承兑汇票详细信息
    'rh_fashenge_chengduihuipiao_detail': {
        # downloader
        'function': 'get_downloader',
        # parser
        'parser_function': 'detail_parser',
        'column_title': request_payload_config.rh_draft_f,
        'table': 'rh_draft_f',
        # next
        'next_processor': 'saver',
        'date_range': ['starttime', 'endtime'],
        'next_parama_list':['draftagreementcode'],
        'detail_point': ['rh_fashenge_hetong_baozheng_list', 'rh_fashenge_hetong_diya_detail',
                         'rh_fashenge_hetong_zhiya_detail'],
    },
    # 发生额信息5.7.0->信用证发生额
    'rh_fashenge_xinyongzheng_list': {
        'function': 'post_downloader',
        'url': 'OweOccurDetailAction.do',
        'payload': json.loads(json.dumps(request_payload_config.rh_fashenge_below_payload) % '6'),
        # parser
        'parser_function': 'list_parser',
        'table_header': True,
        'table_footer': True,
        # next
        # rh_fashenge_piaojutixian_detail  票据贴现发生额->借款人票据贴现详细信息
        'detail_point': ['rh_fashenge_xinyongzheng_detail'],
    },
    # 发生额信息5.7.1->信用证发生额->借款人信用证详细信息
    'rh_fashenge_xinyongzheng_detail': {
        # downloader
        'function': 'get_downloader',
        # parser
        'parser_function': 'detail_parser',
        'column_title': request_payload_config.rh_creditbalance_f,
        'table': 'rh_creditbalance_f',
        # next
        'next_processor': 'saver',
        'date_range': ['starttime', 'endtime'],
        'next_parama_list':['creditcode'],
        'detail_point': ['rh_fashenge_hetong_baozheng_list', 'rh_fashenge_hetong_diya_detail',
                         'rh_fashenge_hetong_zhiya_detail'],
    },
    # 发生额信息5.8.0->保函发生额
    'rh_fashenge_baohan_list': {
        'function': 'post_downloader',
        'url': 'OweOccurDetailAction.do',
        'payload': json.loads(json.dumps(request_payload_config.rh_fashenge_below_payload) % '7'),
        # parser
        'parser_function': 'list_parser',
        'table_header': True,
        'table_footer': True,
        # next
        # rh_fashenge_piaojutixian_detail  票据贴现发生额->借款人票据贴现详细信息
        'detail_point': ['rh_fashenge_baohan_detail'],
    },
    # 发生额信息5.8.1->保函发生额->借款人保函详细信息
    'rh_fashenge_baohan_detail': {
        # downloader
        'function': 'get_downloader',
        # parser
        'parser_function': 'detail_parser',
        'column_title': request_payload_config.rh_guaranteeha_f,
        'table': 'rh_guaranteeha_f',
        # next
        'next_processor': 'saver',
        'next_parama_list':['guaranteecode'],
        'date_range': ['starttime', 'endtime'],
        'detail_point': ['rh_fashenge_hetong_baozheng_list', 'rh_fashenge_hetong_diya_detail',
                         'rh_fashenge_hetong_zhiya_detail'],
    },
}

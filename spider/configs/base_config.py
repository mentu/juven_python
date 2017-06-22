#!/usr/bin/env python
# -*- coding: utf_8 -*-

_redis_ip_ = '127.0.0.1'
_redis_port_ = '6379'
_redis_db_ = '0'

_database_name_ = 'YHJ'
_database_ip_ = '127.0.0.1'
_database_port_ = '3306'
_database_user_ = 'root'
_database_pwd_ = 'hubeixiangyang.0'

request_header = {
    'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    , "Upgrade-Insecure-Requests": "1"
    , "Host": "www.bankersalmanac.com"
    , 'Connection': 'keep-alive'
    , "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    , "Accept-Encoding": "gzip, deflate, sdch, br"
    , "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6"
    , 'Cache - Control':  'max - age = 0'
    , 'Referer': 'https: // www.bankersalmanac.com / formslogin.aspx'
}

root_url = 'https://www.bankersalmanac.com/'

details_url = 'https://www.bankersalmanac.com/private/'

_search_detail_url_ = 'https://www.bankersalmanac.com/private/seaban.aspx'

login_url = 'https://www.bankersalmanac.com/formslogin.aspx'

# login_username = 'bocom1'
# login_password = 'Happy2017'

login_username = 'bocom122'
login_password = 'china'

_full_details_ = {
    'head_office_details': {
        'table': 'head_office_details',
        'tag': 'div',
        'element': 'class',
        'element_value': 'ContactDetails'
    }
}

head_office_details = ['fid', 'address', 'tel', 'tgms', 'swift', 'reuters', 'chips_uid', 'website']
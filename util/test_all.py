#-*-coding:utf-8-*-

from selenium import webdriver
from selenium import webdriver
# driver = webdriver.PhantomJS()
# driver.get("http://www.csdn.net")
# data = driver.title
# driver.save_screenshot('csdn.png')
# print data

import os
import getpass
print getpass.getuser()

# if not os.path.exists("./d1"):
#     os.mkdir("./d1")
#
# from configs import base_config
# from configs import mylog
#
# print base_config._database_ip_
# logger=mylog.MyLog()
# logger.info("写到了哪里？调用MyLog的脚本所在的目录==")


import xlrd
import sys


reload(sys)
sys.setdefaultencoding('utf-8')
data = xlrd.open_workbook('./excel/all_cust_list.xlsx')

sheet = data.sheet_by_index(0)
list=[]
for v in sheet.col_values(0,1):
    list.append(v)

print list


#-*-coding:utf-8-*- 

import scrapy
import random 
import ast

import pymongo
from scrapy.spiders import Spider
from landinfo.items import Land
from landinfo.settings import PROXIES, MONGODB_SERVER,MONGODB_PORT,MONGODB_DB,MONGODB_COLLECTION
from scrapy.selector import Selector
from datetime import datetime



class land(Spider):

    name = "land"
    start_urls = ["http://www.landchina.com/default.aspx?tabid=263"]

    cur = 0
    conditionData = ''
    state = ''
    dis_code = ''
    city = ''

    connection = pymongo.MongoClient(MONGODB_SERVER,
                                     MONGODB_PORT)
    db = connection[MONGODB_DB]
    collection = db[MONGODB_COLLECTION]

    # Get parameter passed from land_main.py
    def __init__(self, district='', date_from='', date_to='', dist_list=dict(), *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        self.filter_date_from = date_from
        self.filter_date_to = date_to
        self.filter_district = district
        self.dist_dict_list = dist_list

    # Modify the request parameters according to filter information 
    def filter(self, response):

        print ",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,"
        print self.filter_district
        print self.filter_date_from 
        print self.filter_date_to
        

    	if self.filter_date_from != '':
            conditionItem270 = Selector(response).xpath('//input[@id="TAB_QueryConditionItem270"]/@value').extract()[0]
            self.conditionData += "|" + conditionItem270.encode('ascii','ignore') + ":%s~%s"% (self.filter_date_from,self.filter_date_to)

        if self.filter_district != '':
            self.city = self.filter_district
            for dist in self.dist_dict_list:
                if dist['name'] == self.filter_district:
                    self.dis_code = dist['value']
                    break 
            if self.dis_code == '':
                raise Exception("Wrong input for district")
            if len(self.dis_code) == 2:
                self.city = ''
                self.state = self.filter_district
            else:
                statecode = self.dis_code[0:2]
                for state in self.dist_dict_list:
                    if state['value'] == statecode:
                        self.state = state['name']
                        break 
            conditionItem256 = Selector(response).xpath('//input[@id="TAB_QueryConditionItem256"]/@value').extract()[0]
            dist_pref =  "|" + conditionItem256.encode('ascii','ignore') + ":%s%%~" % self.dis_code
            dist_name = unicode(self.filter_district,"utf-8").encode("utf8")
            self.conditionData += dist_pref + dist_name 


    # Get the first page after filtering. 
    def parse(self, response):

        self.conditionData = ''
        self.filter(response)
        yield scrapy.FormRequest.from_response(response,
                            formdata={'TAB_QuerySubmitPagerData':'1', 
                            'TAB_QuerySubmitConditionData': self.conditionData},
                            dont_filter = True, callback=self.parse_all_page)


    def parse_all_page(self,response):

            
        pager = ''.join(response.xpath("//table/tbody/tr/td[@class='pager'][1]/text()").extract())
        try: 
            # Get information of total number of pages 
            last_page_par = pager.split()[0]
            end_page = eval(''.join(ele for ele in last_page_par if ele.isdigit()))
        except:
            # If no total pages is given, default end page number if 1. 
            end_page = 1

        # Using page numbers as parameter, yield requests concurrently. 
    	for idx in xrange(1, end_page + 1):
    		yield scrapy.FormRequest.from_response(response,
                            formdata={'TAB_QuerySubmitPagerData':str(idx), 
                            'TAB_QuerySubmitConditionData': self.conditionData},
                            dont_filter = True, callback=self.parse_page)

    # For each page, get the urls (30 per page)
    def parse_page(self,response):
        rows = response.xpath("//table[@id='TAB_contentTable']/tbody/tr")
        for row in rows: 
            rel_url = ''.join(row.xpath('td[@class="queryCellBordy"][2]/a/@href').extract())
            abs_url = response.urljoin(rel_url)

            # Check duplicates. 
            if self.collection.find_one({"项目链接":abs_url}) is not None:
            	print "<<<<<<<<<<<Catch Duplicate<<<<<<<<<"
            	continue
            
            item = Land()
            item['url'] = abs_url
            req = scrapy.Request(abs_url, callback=self.parse_item) 
            req.meta['foo'] = item
            yield req 

    # Parse each url, yield items
    def parse_item(self,response):

        if self.collection.find_one({"项目链接":response.url}) is not None:
            print "<<<<<<<<<<<Catch Duplicate<<<<<<<<<"
            return 
        item = response.meta['foo']

        prefix = "//span[@id='mainModuleContainer_1855_1856_ctl00_ctl00_p1_"
        item['district'] = ''.join(response.xpath(prefix + "f1_r1_c2_ctrl']/text()").extract())
        if item['district'] == '':
            return
        item['e_num'] = ''.join(response.xpath(prefix + "f1_r1_c4_ctrl']/text()").extract())
        item['project'] = ''.join(response.xpath(prefix + "f1_r17_c2_ctrl']/text()").extract())
        item['loc'] = ''.join(response.xpath(prefix + "f1_r16_c2_ctrl']/text()").extract())
        item['area'] = ''.join(response.xpath(prefix + "f1_r2_c2_ctrl']/text()").extract())
        item['land_usage'] = ''.join(response.xpath(prefix + "f1_r3_c2_ctrl']/text()").extract())
        item['time_limit'] = ''.join(response.xpath(prefix + "f1_r19_c2_ctrl']/text()").extract())
        item['sup_method'] = ''.join(response.xpath(prefix + "f1_r3_c4_ctrl']/text()").extract())
        item['category'] = ''.join(response.xpath(prefix + "f1_r19_c4_ctrl']/text()").extract())
        item['level'] = ''.join(response.xpath(prefix + "f1_r20_c2_ctrl']/text()").extract())
        item['price'] = ''.join(response.xpath(prefix + "f1_r20_c4_ctrl']/text()").extract())
        item['sign_date'] = ''.join(response.xpath(prefix + "f1_r14_c4_ctrl']/text()").extract())
        item['right_holder'] = ''.join(response.xpath(prefix + "f1_r9_c2_ctrl']/text()").extract())
        item['plot_ratio_lower'] = ''.join(response.xpath(prefix + "f2_r1_c2_ctrl']/text()").extract())
        item['plot_ratio_upper'] = ''.join(response.xpath(prefix + "f2_r1_c4_ctrl']/text()").extract())
        item['t_date'] = ''.join(response.xpath(prefix + "f1_r21_c4_ctrl']/text()").extract())
        item['arr_start_date'] = ''.join(response.xpath(prefix + "f1_r22_c2_ctrl']/text()").extract())
        item['arr_end_date'] = ''.join(response.xpath(prefix + "f1_r22_c4_ctrl']/text()").extract())
        item['authorized'] = ''.join(response.xpath(prefix + "f1_r14_c2_ctrl']/text()").extract())
        item['state'] = self.state
        item['city'] = self.city
        item['code'] = self.dis_code
      
        # Algorithm for land source is obatined from page source 
        areaS2V = ''.join(response.xpath(prefix + "f1_r2_c4_ctrl']/text()").extract())
        if areaS2V == item['area']: 
            item['land_source'] = "现有建设用地"
        elif eval(areaS2V) == 0:
            item['land_source'] = "新增建设用地"
        else:
            item['land_source'] = "新增建设用地(来自存量库)"

        if (item['authorized'] != '') and (u'人民政府' not in item['authorized']):
            item['authorized'] += u'人民政府'

        land_dict = dict()
        land_dict['行政区'] = item['district']
        land_dict['电子监管号'] = item['e_num']
        land_dict['项目名称'] = item['project']
        land_dict['项目位置'] = item['loc']
        land_dict['面积(公顷)'] = item['area']
        land_dict['土地来源'] = item['land_source']
        land_dict['土地用途'] = item['land_usage']
        land_dict['供地方式'] = item['sup_method']
        land_dict['土地使用年限'] = item['time_limit']
        land_dict['行业分类'] = item['category']
        land_dict['土地级别'] = item['level']
        land_dict['成交价格(万元)'] = item['price']
        land_dict['土地使用权人'] = item['right_holder']
        land_dict['约定容积率下限'] = item['plot_ratio_lower']
        land_dict['约定容积率上限'] = item['plot_ratio_upper']
        land_dict['约定交地时间'] = item['t_date']
        land_dict['约定开工时间'] = item['arr_start_date']
        land_dict['约定竣工时间'] = item['arr_end_date']
        land_dict['批准单位'] = item['authorized']
        land_dict['合同签订日期'] = item['sign_date']
        land_dict['省'] = item['state']
        land_dict['市'] = item['city']
        land_dict['城市代码'] = item['code']
        land_dict['项目链接'] = item['url']

        print "--------------------------cur-------------------------------"
        self.cur += 1
        print "cur = %d" %self.cur

        self.collection.insert(land_dict)

        yield item
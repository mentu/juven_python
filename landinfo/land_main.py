
#-*-coding:utf-8-*- 
import json
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from landinfo.spiders.land import land

import ast
from datetime import date, timedelta, datetime
import time

def main(dist='', from_date=date(2015,11,1), to_date=date.today()):

    with open(u'中国土地市场的省份代码数据.txt') as file_object:
        all_the_text = file_object.read()
    districts = ''.join(all_the_text.split()).replace('][',',').replace('true','True').replace('false','False')
    dist_dict_list = ast.literal_eval(districts)

    spider = land()
    # 10天一个轮循
    delta = timedelta(days=10) 
    configure_logging()
    runner = CrawlerRunner(get_project_settings())

    
    @defer.inlineCallbacks
    def crawl():
        # if specific city is given, only scrapy information according to date_from and date_to
        if dist != '':
            cur_crawl_from = from_date
            while cur_crawl_from < to_date:
                cur_crawl_to = cur_crawl_from + delta
                yield runner.crawl(spider, district=dist, date_from=str(cur_crawl_from), date_to=str(cur_crawl_to),
                                        dist_list=dist_dict_list)
                cur_crawl_from = cur_crawl_to
        # If specific city is not given, then scrapy information of all districts according 
        # to date_from and date_to 
        else: 
            cur_crawl_from = from_date
            idx = 1
            while cur_crawl_from < to_date:
                cur_crawl_to = cur_crawl_from + delta
                for dist_info in dist_dict_list:
                    # Skip all states. 
                    if len(dist_info['value']) <= 2:
                        continue
                    else:
                        yield runner.crawl(spider, district=dist_info['name'], date_from=str(cur_crawl_from),
                                           date_to=str(cur_crawl_to), dist_list=dist_dict_list)
                cur_crawl_from = cur_crawl_to
                if idx % 30 == 0:
                    time.sleep(100)

        reactor.stop()  

    crawl()
    reactor.run()
    

    print '----------over-----------------'


config_filename = 'landinfo_config.json'
with open(config_filename, 'r') as fr:
    content_dict = json.load(fr)

translate_dict = {'dist':u'行政区', 'from_date':u'签订日期从', 'to_date':u'签订日期到'}
input_dict = {}

for key in translate_dict:
    if key!=u'代理':
        if key in ['from_date', 'to_date']:
            # if content_dict[translate_dict[key]]=='':
            #     continue
            input_dict[key] = datetime.strptime(
                content_dict[translate_dict[key]].encode('utf-8'),'%Y-%m-%d').date()
        else:
            input_dict[key] = content_dict[translate_dict[key]].encode('utf-8')

main(**input_dict)

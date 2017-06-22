# -*- coding: utf-8 -*-

import pymongo 
from scrapy.conf import settings
from scrapy import log

from scrapy.exceptions import DropItem


class MongoDBPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            house_dict = dict()
            house_dict['房源介绍'] = item['description']
            house_dict['房源详情URL'] = item['house_url']
            house_dict['房源属性'] = item['house_info']
            house_dict['小区'] = item['community']
            house_dict['小区详情URL'] = item['community_url']
            house_dict['小区地址'] = item['address']
            house_dict['建筑面积'] = item['area']
            house_dict['总价'] = item['totalprice']
            house_dict['单价'] = item['unitprice']
            house_dict['中介名称'] = item['agent']
            house_dict['中介详情URL'] = item['agent_url']
            house_dict['优点'] = item['advantage']
            house_dict['城市'] = item['city']
            house_dict['区域'] = item['district']
            house_dict['采集时间'] = item['collection_time']

        matching_item = self.collection.find_one({"房源详情URL": item['house_url']})
        if matching_item is not None:
            raise DropItem("Duplicate item found")
        else:
            self.collection.insert(house_dict)
            


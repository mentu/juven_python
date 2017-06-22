#-*-coding:utf-8-*- 

import scrapy
import random
import time 

from datetime import datetime
from houseinfo.settings import PROXIES

from scrapy.spiders import Spider
from scrapy.selector import Selector
from houseinfo.items import House



class house(Spider):

    name = "house"
    start_urls = ["http://esf.fang.com/house/i31/"]

    city_url = start_urls[0]
    cur = 0
    restarts = 0
    max_restarts = 2
    
    def __init__(self, city='', *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        self.city = city

    # Get the index page of cities 
    def parse(self,response):
        city_list_onpage = response.xpath("//div[@id='cityi010']/a/text()").extract()
        more_city_ind = [i for i, item in enumerate(city_list_onpage) if u'更多城市' in item][0]+1
        indx_url = ''.join(response.xpath("//div[@id='cityi010']/a[%d]/@href" % more_city_ind).extract())
        yield scrapy.Request(response.urljoin(indx_url), callback = self.get_city_url,dont_filter = True)


    # Get the url of city by searching on the index page 
    def get_city_url(self, response):

        blubk_text = response.xpath("//div[@id='c01']/ul/li[@class='blubk']/a/text()").extract()
        blubk_text2 = response.xpath("//div[@id='c01']/ul/li[@class='blubk02']/a/text()").extract()

        if self.city in blubk_text:
            for city in response.xpath("//div[@id='c01']/ul/li[@class='blubk']/a"):
                if [self.city] == city.xpath('text()').extract():
                    self.city_url = ''.join(city.xpath('@href').extract())
        elif self.city in blubk_text2:
            for city in response.xpath("//div[@id='c01']/ul/li[@class='blubk02']/a"):
                if [self.city] == city.xpath('text()').extract():
                    self.city_url = ''.join(city.xpath('@href').extract())
        elif self.city != '':
            raise Exception("Input City Does Not Exist")

        yield scrapy.Request(self.city_url, callback = self.parse_city, dont_filter = True)


    # Get url of districts of the city 
    def parse_city(self,response):
        # The 'if' conditions are for different webpage structures 
    	if response.xpath("//div[@class='qxName']/a") == []:
            for dis in response.xpath("//dt[@id='tags']/a"):
                if ''.join(dis.xpath('@href').extract()) == "javascript:;":
                    pass
                else: 
                    cur_url = response.urljoin(''.join(dis.xpath('@href').extract()))
                    yield scrapy.Request(cur_url, callback = self.parse_district, dont_filter = True)
        else:
            if len(response.xpath("//div[@class='qxName']/a")) <= 1:
                yield scrapy.Request(response.url, callback = self.parse_page, dont_filter = True)
            else: 
                # Do not crawl contents in 不限 to avoid duplicates
                for dis in response.xpath("//div[@class='qxName']/a")[1:]:   
                    cur_url = response.urljoin(''.join(dis.xpath('@href').extract()))
                    cur_dist = ''.join(''.join(dis.xpath('text()').extract()).split())
                    yield scrapy.Request(cur_url, callback = self.parse_district, dont_filter = True)


    # Get url of specific locations in the district 
    def parse_district(self,response):    	
        if len(response.xpath("//p[@id='shangQuancontain']/a")) <= 1 :
            yield scrapy.Request(response.url, callback = self.parse_page, dont_filter = True)
        else: 
            for dis in response.xpath("//p[@id='shangQuancontain']/a")[1:]:
                cur_url = response.urljoin(''.join(dis.xpath('@href').extract()))
                cur_dist2 = ''.join(''.join(dis.xpath('text()').extract()).split())
                yield scrapy.Request(cur_url, callback = self.parse_page, dont_filter = True)

    # Main Parse function 
    def parse_page(self, response):
        houses = response.xpath("//dd[@class='info rel floatr']")
        for house in houses:     

            item = House()
            district_info = response.xpath("//a[@class='term']/text()").extract()
            item['district'] = '/'.join(district_info)
            house_url = house.xpath("p[@class='title']/a/@href").extract()
            item['house_url'] = response.urljoin(''.join(house_url))
            community_url = house.xpath("p[@class='mt10']/a/@href").extract()
            item['community_url'] = response.urljoin(''.join(community_url))
            agent_url = house.xpath("p[@class='gray6 mt10']/a/@href").extract()
            item['agent_url'] = response.urljoin(''.join(agent_url))

            house_info = house.xpath("p[@class='mt12']/text()").extract()
            item['house_info'] = '|'.join(''.join(house_info).split())
            totalprice = house.xpath("div[@class='moreInfo']/p/span/text()").extract()
            item['totalprice'] = ''.join(totalprice).strip(u"/")
            unitprice = house.xpath("div[@class='moreInfo']/p/text()").extract()
            item['unitprice'] = '/'.join(unitprice)
            advantage = house.xpath("div[@class='mt8 clearfix']/div[@class='pt4 floatl']/span/text()").extract()
            print advantage
            item['advantage'] = ','.join(advantage)

            item['city'] = Selector(response).xpath('//input[@id="strCity1"]/@value').extract()[0]
            item['address'] = ''.join(house.xpath("p[@class='mt10']/span/text()").extract())
            item['community'] = ''.join(house.xpath("p[@class='mt10']/a/span/text()").extract())
            item['description'] = ''.join(house.xpath("p[@class='title']/a/text()").extract())
            item['area'] = ''.join(house.xpath("div[@class='area alignR']/p[1]/text()").extract())
            item['agent'] = ''.join(house.xpath("p[@class='gray6 mt10']/a/text()").extract())
            item['collection_time'] = str(datetime.now().replace(microsecond=0))


            print "--------------------------cur-------------------------------"
            self.cur += 1
            print "cur = %d" %self.cur

            yield item

        # Flip to next page 
        next_page = response.xpath("//a[@id='PageControl1_hlk_next']/@href").extract()
        if next_page:
            abs_next = response.urljoin(next_page[0])    
            yield scrapy.Request(abs_next, callback=self.parse_page)



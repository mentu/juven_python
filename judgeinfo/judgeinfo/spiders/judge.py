#-*-coding:utf-8-*- 

import scrapy
import pymongo
from scrapy.spiders import Spider
from scrapy.selector import Selector
# from judgeinfo.items import Judge
# from judgeinfo.settings import PROXIES
from ..items import Judge
from ..settings import PROXIES


from scrapy.conf import settings
import random



import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class judge(Spider):

    name = "judge"

    start_urls = [("http://wenshu.court.gov.cn/List/List?"
                  "sorttype=1&conditions=searchWord+2+AJLX++案件类型:民事案件")]

    filtered_url = ("http://wenshu.court.gov.cn/List/List?"
                  "sorttype=1&conditions=searchWord+2+AJLX++案件类型:民事案件")

    main_url = 'http://wenshu.court.gov.cn'

    cur_doc = 0
    cur = 0
    url_set = set()

    connection = pymongo.MongoClient(settings['MONGODB_SERVER'],
                                     settings['MONGODB_PORT'])
    db = connection[settings['MONGODB_DB']]
    collection = db[settings['MONGODB_COLLECTION']]


    # Page number is 25 because the site do not allow access to pages after 25. 
    pagenum = 25

    def __init__(self, keyword='', cause='', court = '', region = '', year = '', procedure = '', doc_type = '', advanced_filter = [],  *args, **kwargs):
        super(Spider, self).__init__(*args, **kwargs)
        self.keyword= keyword   
        self.cause = cause
        self.court = court 
        self.region = region
        self.year = year 
        self.procedure = procedure 
        self.doc_type = doc_type
        self.advanced_filter = advanced_filter

    # Modify the url according to filter conditions, if given 
    def filter(self):
        if self.advanced_filter != []:
            filter_info = '%20'.join(self.advanced_filter)
            self.filtered_url += "&conditions=searchWord+QWJS+++全文检索:%s" % (filter_info)
        if self.keyword != '':
            self.filtered_url += "&conditions=searchWord+%s+++关键词:%s" % (self.keyword,self.keyword)
        if self.cause != '':
            self.filtered_url += "&conditions=searchWord+%s+++一级案由:%s" % (self.cause, self.cause)
        if self.court != '':
            self.filtered_url += "&conditions=searchWord+%s+++法院层级:%s" % (self.court, self.court)
        if self.region != '':
            self.filtered_url += "&conditions=searchWord+%s+++法院地域:%s" % (self.region, self.region)
        if self.year != '':
            self.filtered_url += "&conditions=searchWord+%s+++裁判年份:%s" % (self.year, self.year)
        if self.procedure != '':
            self.filtered_url += "&conditions=searchWord+%s+++审判程序:%s" % (self.procedure, self.procedure)
        if self.doc_type != '':
            self.filtered_url += "&conditions=searchWord+%s+++文书类型:%s" % (self.doc_type, self.doc_type)



    def get_urls(self):

        self.filter()

        driver = webdriver.Chrome()
        driver.set_window_size(1200, 1024)
        driver.get(self.filtered_url)
        wait = WebDriverWait(driver, 15)
        wait_click = WebDriverWait(driver,2)
        
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='wstitle']/a")))
        except:
            self.logger.info(u'-----------No Elements Available------------------------')
            return

       
        # If total number of item is more than 125, we choose to display 20 items per page (defaul is 5)
        num_item = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@id='span_datacount']"))).text
        if eval(num_item) > 125: 
            for ids in [15,17,19,21]:
                try:
                    time.sleep(1)
                    num_list = wait_click.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='%d_button']" %ids)))
                    driver.execute_script("arguments[0].click();", num_list)
                    time.sleep(1)
                    num_per_page  = wait_click.until(EC.element_to_be_clickable((By.XPATH, "//ul/li[@id='%d_input_20']" %ids)))
                    driver.execute_script("arguments[0].click();", num_per_page)
                    time.sleep(1)
                except:
                    pass     

        idx = 1

        while idx <= self.pagenum:
           
            # Wait for the content to load 
            try:
                wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='wstitle']/a")))
            except:
                # Not all pages are visited due to unstable internet connection 
                self.logger.info(u'---------------Stop at Page %d--------------------' % idx)
                break

            sel = Selector(text=driver.page_source)
            judges = sel.xpath("//div[@class='wstitle']/a")

            # Collect all urls of documents in the set 
            for judge in judges:
                self.url_set.add(''.join(judge.xpath('@href').extract()))

            try: 
                pagedown = wait_click.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='pageNumber']/a[@class='next']")))
                driver.execute_script("arguments[0].click();", pagedown)
            except:
                self.logger.info(u'---------------Cannot Get Next Page--------------------')
                break 

            idx += 1

        driver.quit()


    def start_requests(self):
        

        # Build the url set 
        self.get_urls()

        # Request all document url 
        for url in self.url_set:
            abs_url = self.main_url + url[0:url.find("&")]
            if self.collection.find_one({"链接":abs_url}) is None:
                yield scrapy.Request(abs_url, callback=self.parse, dont_filter = True,
                            errback = lambda x: self.download_errback(x, abs_url))
        

    # If downloading document page gets error 
    def download_errback(self, e, url):
        print "<<<<<<<<<<<<<<<<<ERROR<<<<<<<<<<<<<<<<<<<"
        print url
        print e

    # Get basic info of the documents, and request document text page url 
    def parse(self,response):

        docID = response.url[response.url.find("=")+1:]
        docURL = '/content/content?DocID=' + docID
        if self.collection.find_one({"链接":response.url}) is not None:
            print "<<<<<<<<<<<Catch Duplicate<<<<<<<<<"
            return

        print "----------------------------- Cur -----------------------"
        self.cur += 1
        print response.url
        print self.cur
        
        item = Judge()
        item['case_name'] = ''.join(Selector(response).xpath("//input[@id='hidCaseName']/@value").extract())
        item['case_num'] = ''.join(Selector(response).xpath("//input[@id='hidCaseNumber']/@value").extract())
        item['url'] = response.url
        dic_string_unmod = Selector(response).xpath("//input[@id='hidCaseInfo']/@value").extract()[0]
        dic_string = ''.join(dic_string_unmod.replace('null','None').split())
        item['case_info'] = eval(dic_string)['诉讼记录段原文']
        item['procedure'] = eval(dic_string)['审判程序']
        item['court'] = ''.join(Selector(response).xpath("//input[@id='hidCourt']/@value").extract())
        item['company'] = self.advanced_filter[0]
        docID = Selector(response).xpath("//input[@id='hidDocID']/@value").extract()
        doc_text_url = "http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID="+''.join(docID)
        doc_url = "http://wenshu.court.gov.cn/content/content?DocID=" + ''.join(docID)
        req = scrapy.Request(doc_text_url, callback=self.parse_doc, dont_filter=True, 
                            errback = lambda x: self.download_errback(x, doc_url))
        req.meta['foo'] = item
        yield req


    # Get the original text of the document
    def parse_doc(self,response):

        docID = response.url[response.url.find("=")+1:]
        docURL = '/content/content?DocID='  + docID

        item = response.meta['foo']
        item['text'] = '\n\t'.join(response.xpath("/html/body/div/text()").extract())
        matching_item = self.collection.find_one({"链接": item['url'],"案件名称":item['case_name'], '案号': item['case_num'] })
        if matching_item is not None:
            print "<<<<<<<<<<<Catch Duplicate<<<<<<<<<"
            return
        if item['text'] == '':
            print "---------------------Crawler is banned : sleep and wait -----------------"
            print response.url
            time.sleep(10)
            request = scrapy.Request(self.main_url + docURL, callback=self.parse, dont_filter=True, 
                                    errback = lambda x: self.download_errback(x, self.main_url + docURL),
                                    meta={'proxy':"http://%s" % random.choice(PROXIES)['ip_port']})
            yield request 
            return 

        judge_dict = dict()
        judge_dict['案件名称'] = item['case_name']
        judge_dict['案号'] = item['case_num']
        judge_dict['链接'] = item['url']
        judge_dict['诉讼记录段原文'] = item['case_info']
        judge_dict['法院名称'] = item['court']
        judge_dict['审判程序'] = item['procedure']
        judge_dict['全文'] = item['text']
        judge_dict['公司名称'] = item['company']

        self.logger.info(u'---------------Current Doc ----------------')
        self.cur_doc += 1
        self.collection.insert(judge_dict)
        print response.url
        print self.cur_doc
        yield item



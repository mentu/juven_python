#-*-coding:utf-8-*- 
import json
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from judgeinfo.spiders.judge import judge



def main(keyword='',cause='',court='', region = '', year = '', procedure = '', doc_type = '', advanced_filter = []):
	
	# Clients.txt contains a list of company names. 
	file_object = open('clients.txt')
	all_the_text = file_object.read()
	clients = all_the_text.split()


	spider = judge()
	configure_logging()
	runner = CrawlerRunner(get_project_settings())

	@defer.inlineCallbacks
	def crawl():
		# Use company names in clients.txt, pass them as inputs of advanced filter. 
		for client in clients: 
			yield runner.crawl(spider, keyword=keyword,cause=cause,court=court, region = region, 
							year = year, procedure = procedure, doc_type = doc_type, advanced_filter = [client])
		reactor.stop()  

	crawl()
	reactor.run()

	print '----------over-----------------'

config_filename = 'judgeinfo_config.json'
with open(config_filename, 'r') as fr:
	content_dict = json.load(fr)

translate_dict = {'keyword':u'关键词', 'cause':u'案由', 'court':u'法院层级',
				  'region':u'法院地域', 'year':u'年份', 'procedure':u'审判程序',
				  'doc_type':u'文书类型',}
input_dict = {}
for key in translate_dict:
	input_dict[key] = content_dict[translate_dict[key]].encode('utf-8')

main(**input_dict)

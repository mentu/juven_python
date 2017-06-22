#-*-coding:utf-8-*- 
import json
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging

from houseinfo.spiders.house import house


def main(city = u''):

	spider = house()

	configure_logging()
	runner = CrawlerRunner(get_project_settings())

	@defer.inlineCallbacks
	def crawl():
		yield runner.crawl(spider, city = city)
		reactor.stop()  

	crawl()
	reactor.run()

	print '----------over-----------------'

config_filename = 'houseinfo_config.json'
with open(config_filename, 'r') as fr:
	content_dict = json.load(fr)

translate_dict = {'city':u'城市'}
input_dict = {}
for key in translate_dict:
	input_dict[key] = content_dict[translate_dict[key]]

main(**input_dict)

import scrapy
from scrapy.spiders import Spider
from scrapy.selector import Selector
from ippool.items import Ip


class ip(Spider):
	name = 'ip'
	start_urls = ["http://www.xicidaili.com/nn/"]

	ip_set = set()
	# 需要ip地址的数量
	ip_needed = 300 

	def parse(self,response):
		
		ips = response.xpath('//tr')

		if len(self.ip_set) < self.ip_needed:

			# Get IPs by xpath. 
			for ip in ips[1:]:
				ip_type = ip.xpath("td[6]/text()").extract()
				ip_speed = ip.xpath("td[@class='country'][3]/div[@class='bar']/div[@class='bar_inner fast']").extract()
				if ip_type == [u'HTTP'] and ip_speed != []:
					ip_address = ip.xpath('td[2]/text()').extract()
					port = ip.xpath('td[3]/text()').extract()
					item = Ip()
					item['ip_port'] = ':'.join(ip_address + port)
					self.ip_set.add(item['ip_port'])
					yield item

			# 翻页
			next_url = ''.join(response.xpath("//a[@class='next_page']/@href").extract())
			yield scrapy.Request(response.urljoin(next_url), callback = self.parse)
		



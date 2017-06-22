import scrapy
from scrapy import Item, Field, Request


class House(Item):
	description = Field()
	house_url = Field()
	house_info = Field()
	community = Field()
	community_url = Field()
	address = Field()
	area = Field()
	totalprice = Field()
	unitprice = Field()
	agent = Field()
	agent_url = Field()
	advantage = Field()
	city = Field()
	collection_time = Field()
	district = Field()
	district2 = Field()



    



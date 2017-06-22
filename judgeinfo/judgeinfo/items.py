import scrapy
from scrapy import Item, Field, Request

class Judge(Item):
	case_name = Field()
	case_num = Field()
	legal_person = Field()
	url = Field()
	case_info = Field()
	court = Field()
	procedure = Field()
	text = Field()
	company = Field()



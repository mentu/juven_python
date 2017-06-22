import scrapy
from scrapy import Item, Field, Request

class Ip(Item):
    ip_port = Field()
    

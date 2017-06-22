import scrapy
from scrapy import Item, Field, Request


class Land(Item):
	district = Field()
	e_num = Field()
	project = Field()
	loc = Field()
	area = Field()
	land_source = Field()
	land_usage = Field()
	sup_method = Field()
	time_limit = Field()
	category = Field()
	level = Field()
	price = Field()
	right_holder = Field()
	plot_ratio_lower = Field()
	plot_ratio_upper = Field()
	t_date = Field()
	arr_start_date = Field()
	arr_end_date = Field()
	authorized = Field()
	sign_date = Field()
	state = Field()
	city = Field()
	code = Field()
	url = Field()


    



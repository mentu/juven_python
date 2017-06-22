#-*-coding:utf-8-*-

import ast
from collections import OrderedDict

with open(u'中国土地市场的省份代码数据.txt', 'r') as file_object:
    all_the_text = file_object.read()
districts = ''.join(all_the_text.split()).replace('][',',').replace('true','True').replace('false','False')
dist_dict_list = ast.literal_eval(districts)

dist_dict = OrderedDict({'省级行政区':[], '市级行政区':[]})
for item in dist_dict_list:
    if len(item['value']) == 2:
        dist_dict['省级行政区'].append(item['name'])
    elif len(item['value']) > 2:
        dist_dict['市级行政区'].append(item['name'])

with open(u'中国行政区列表.txt', 'w') as fw:
    for key in dist_dict:
        fw.write(key+'：\n')
        for item in dist_dict[key]:
            fw.write(item+'\n')
        fw.write('\n')
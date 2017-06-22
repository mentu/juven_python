#!/usr/bin/env python
# coding: utf-8
__author__ = 'yueyt'

import time
import os
import re
from bs4 import BeautifulSoup
from config_tt.base_config import page_encoding
# from config_tt import  request_payload_config
from config_tt.log_config import logger


class CreditParser(object):
    def __init__(self, queue):
        self.queue = queue

    @staticmethod
    def _get_data_table(response, table_selector, current_processor):
        """获取含数据的table"""
        if not response:
            return
        try:
            soup = BeautifulSoup(response.content, 'html.parser', from_encoding=page_encoding)
        except AttributeError as e:
            soup = BeautifulSoup(response, 'html.parser', from_encoding=page_encoding)
        records = soup.select(table_selector)
        table_number = current_processor.get('table_number')
        if table_number:
            try:
                records = [(records[table_number])]
            except IndexError as e:
                logger.error('{}'.format(e.args))
                return
        return records

    @staticmethod
    def get_page_title(response):
        if not response:
            return
        soup = BeautifulSoup(response.content, 'html.parser', from_encoding=page_encoding)

        title = soup.title.string if soup.title else ''
        if title:
            title = title.strip()
        return title

    @staticmethod
    def _get_detail_urls(records):
        """获取href链接URL"""
        urls = []

        if not records or len(records) == 0:
            return urls

        for record in records:
            rows = record.select('td')
            for col in rows:
                href_tag = col.select_one('a[href]')
                if href_tag and href_tag.get('href') != '#':
                    urls.append(href_tag.get('href'))
                # 获取js点击的href 参数
                href_onclick = col.get('onclick')
                if not href_onclick and href_tag:
                    href_onclick = href_tag.get('onclick')
                if href_onclick:
                    href_onclick = href_onclick.replace('javascript:', '').replace(';', '')
                    urls.append(href_onclick)
        return list(set(urls))

    @staticmethod
    def _get_list_values(tables, current_processor):
        """获取列表值"""
        result_list = []
        if not tables or len(tables) == 0:
            return result_list

        for t in tables:
            records = t.find_all('tr', attrs=current_processor.get('special_rows_tr_attrs'), )
            # 去除表头和总计表尾
            if records:
                if current_processor.get('table_header'):
                    records = records[1:]
                if current_processor.get('table_footer'):
                    records = records[:-1]
            for record in records:
                r = []
                rows = record.select('td')
                if not rows or len(rows) == 0:
                    continue

                for col in rows:
                    if col.findChildren():
                        v = col.findChildren()[-1].string
                        if v:
                            r.append(v.strip())
                        else:
                            r.append(v)
                    else:
                        r.append(col.string.strip())
                result_list.append(r)
        return result_list

    @staticmethod
    def _get_detail_values(records):
        """获取detail值"""
        detail_values = []
        if not records or len(records) == 0:
            return detail_values

        for n, record in enumerate(records):
            if n % 2 == 1:
                if record.string:
                    detail_values.append(record.string.strip())
                else:
                    detail_values.append('')
        return detail_values

    def _get_column_value_mapping(self, current_processor, list_values, passvalue):
        """根据列名和值，返回dict"""
        list_infos = []
        next_parama_list = []
        if not current_processor.get('column_title') or not list_values:
            return list_infos, next_parama_list

        for list_value in list_values:
            list_info = dict(zip(current_processor.get('column_title'), list_value))
            next_parama = {}
            # 额外增加的字段（表名，中征码和curr_parama_list配置的列名）
            list_info['midsigncode'] = passvalue.get('loancard')
            os.environ['midsigncode'] = passvalue.get('loancard')
            list_info['table'] = current_processor.get('table')
            list_info['uploadtime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            if current_processor.get('add_searchdate'):
                # list_info['searchdate'] = request_payload_config.last_quarter_end
                list_info['searchdate'] = os.getenv('last_quarter_end')
            for cp in current_processor.get('curr_parama_list', ''):
                if passvalue.get(cp):
                    list_info[cp] = passvalue.get(cp)
            for time_range in current_processor.get('date_range', ''):
                if time_range:
                    list_info['starttime'] = os.getenv('last_quarter_start')
                    list_info['endtime'] = os.getenv('last_quarter_end')
            # for cp in current_processor.get('curr_parama_list', ''):
            #     if passvalue.get(cp):
            #         list_info[cp] = passvalue.get(cp)

            # 列名重命名
            rename_column_mapping = current_processor.get('rename_column_mapping', {})
            for colname in rename_column_mapping:
                if colname in list_info:
                    list_info[rename_column_mapping[colname]] = list_info.pop(colname)
            list_infos.append(list_info)

            # 处理传递的参数
            for np in current_processor.get('next_parama_list', ''):
                if list_info.get(np):
                    next_parama[np] = list_info.get(np)
            next_parama_list.append(next_parama)

        return list_infos, next_parama_list

    def _route_one_point_one_url(self, point, url, passvalue, response=None):
        if not point:
            return

        if response:
            self.queue.put([point, url, passvalue, response])
        else:
            self.queue.put([point, url, passvalue])

    def _route_one_point_many_urls(self, point, urls, passvalue, other_passvalue_list, rsp):
        try:
            for index, url in enumerate(urls):
                new_passvalue = dict(passvalue)
                if other_passvalue_list and other_passvalue_list[index]:
                    for key in other_passvalue_list[index]:
                        new_passvalue[key] = other_passvalue_list[index].get(key)
                self._route_one_point_one_url(point, url, new_passvalue, rsp)
        except Exception as e:
            logger.error("超出数组范围！", e)

    def _route_many_points_many_urls(self, points, urls, passvalue, other_passvalue_list=None, rsp=None):
        if not points:
            return

        if not urls and not ['']:
            return

        for point in points:
            self._route_one_point_many_urls(point, urls, passvalue, other_passvalue_list, rsp)

    def _route_next_page(self, response, processor_type, passvalue):
        """翻页，下一页"""
        if not response:
            return
        regx = re.compile(r"showRoll\(.*\)")
        result = re.findall(regx, response.text)
        if result:
            exec("from config_tt.processor_config import *")
            payload = eval(result[0])
            if int(payload.get('currentPage', '0')) < int(payload.get('pageCount', '0')):
                payload['currentPage'] = '{}'.format(int(payload.get('currentPage')) + 1)
                # return payload
                new_passvalue = dict(passvalue)
                new_passvalue.update(payload)
                self._route_one_point_one_url(processor_type, [''], new_passvalue)

    def list_parser(self, processor_type, current_processor, response, passvalue):
        """list 解析"""
        if not response:
            logger.error('processor_type:{}, passvalue:{}'.format(processor_type, passvalue))
            return

        # 获取配置参数
        table_selector = current_processor.get('table_selector') or 'table#list'

        # 获取数据记录
        records = self._get_data_table(response, table_selector, current_processor)
        list_values = self._get_list_values(records, current_processor)
        if current_processor.get('tr_select'):
            for i in list_values:
                if len(i) == current_processor.get('tr_select'):
                    list_values = list_values
                else:
                    list_values = []
        # 获取入库字段和值
        list_infos, next_param_list = self._get_column_value_mapping(current_processor, list_values, passvalue)

        # 钻取详情
        detail_urls = [''] if current_processor.get('ignore_detail_urls') else self._get_detail_urls(records)
        #判断是否讲response传入下一级
        if not current_processor.get('next_response'):
            self._route_many_points_many_urls(current_processor.get('detail_point'),
                                          detail_urls, passvalue, next_param_list)
        if current_processor.get('next_response'):
            self._route_many_points_many_urls(current_processor.get('detail_point'),
                                              [''], passvalue, next_param_list, response)

        # 获取列表的下一页
        self._route_next_page(response, processor_type, passvalue)

        return list_infos

    def detail_parser(self, processor_type, current_processor, response, passvalue):
        """detail 解析"""
        if not response:
            logger.error('processor_type:{}, passvalue:{}'.format(processor_type, passvalue))
            return

        # 获取配置参数
        table_selector = current_processor.get('table_selector') or 'table#list > tbody > tr > td'

        # 获取数据记录
        records = self._get_data_table(response, table_selector, current_processor)

        detail_values = self._get_detail_values(records)
        # 获取入库字段和值
        list_infos, next_param_list = self._get_column_value_mapping(current_processor, [detail_values], passvalue)

        # 钻取详情
        self._route_many_points_many_urls(current_processor.get('detail_point'),
                                          [''], passvalue, next_param_list, response)

        return list_infos

    def mix_list_parser(self, processor_type, current_processor, response, passvalue):
        """list 解析"""
        if not response:
            logger.error('processor_type:{}, passvalue:{}'.format(processor_type, passvalue))
            return

        # 获取配置参数
        table_selector = current_processor.get('table_selector') or 'table#list'

        # 获取数据记录
        records = self._get_data_table(response, table_selector, current_processor)
        list_values = self._get_list_values(records, current_processor)

        # 获取入库字段和值
        list_infos, next_param_list = self._get_column_value_mapping(current_processor, list_values, passvalue)

        return list_infos

    def double_parser(self, processor_type, current_processor, response, passvalue):
        '''对于一个表格里面需要拆分的处理'''
        if not response:
            logger.error('processor_type:{}, passvalue:{}'.format(processor_type, passvalue))
            return

        # 获取配置参数
        table_selector = current_processor.get('table_selector') or 'table#list'

        # 获取数据记录
        records = self._get_data_table(response, table_selector, current_processor)
        list_values = self._double_parser(records, current_processor)

        # 获取入库字段和值
        list_infos, next_param_list = self._get_column_value_mapping(current_processor, list_values, passvalue)

        return list_infos

    def _double_parser(self, tables, current_processor):
        '''对于同一个表格里面需要解析两种结果的处理函数
            针对担保信息里面（抵押人和自然抵押人信息处理）
        '''
        result_dict = {}
        if tables:
            for i in tables:
                result = []
                for n in i.find_all("td"):
                    result.append(n.string.strip() if n.string else '')
                if len(result) == 4:
                    result_dict[4] = result
                elif len(result) == 5:
                    result_dict[5] = result
            if result_dict.get(current_processor.get('tr_select'), []):
                return [result_dict.get(current_processor.get('tr_select'), [])]
            else:
                return []
        else:
            return []

    def re_add_post__parser(self, processor_type, current_processor, response, passvalue):
        '''
            正则匹配出所需要的post的表单数据
        '''
        if not response:
            logger.error('processor_type:{}, passvalue:{}'.format(processor_type, passvalue))
            return
        import re
        content = response.text
        loanid = []
        loanid_list = re.findall("\(\'\d+\'\)", content)  # 获取loanid的id
        for i in loanid_list:
            loanid.append(str(i)[2])
        financecode = re.search('financecode\=\d+', content)
        financecode = financecode.group().split('=')[1] if financecode else ''
        loancardcode = re.search('\+.*\d+.?\+', content)
        loancardcode = loancardcode.group().split('+')[1].strip() if loancardcode else ''
        if current_processor.get("re_type"):
            contractcode = re.search('contractcode=[0-9A-Z]+', content)
            contractcode = contractcode.group().split('=')[1] if contractcode else ''
        else:
            contractcode = re.search('constr .*\= .*\;', content)
            contractcode = contractcode.group().split("'")[1].encode('gbk') if contractcode else  ''
        #loandb=1 担保  loandb=2 被担保  dzy=1 保证 2 抵押 3 质押
        dzy = current_processor.get('label_type')
        # loandb = re.search('&loandb\=\d+', content)
        # loandb = loandb.group().split('=')[1] if loandb else ''
        loandb = current_processor.get('loandb_type')
        # print("loanid=",loanid,"financecode=",financecode,"loancardcode=",loancardcode,"contractcode=",contractcode,"loandb=",loandb,'dzy=',dzy)
        # 钻取详情
        for i in loanid:
            next_param_list = [
                {'loanid': i, "financecode": financecode, "loancardcode": loancardcode, "contractcode": contractcode,
                 'dzy': dzy, 'loandb': loandb}]
            self._route_many_points_many_urls(current_processor.get('detail_point'),
                                              [''], passvalue, next_param_list)
        return ''

    def goods_parser(self, processor_type, current_processor, response, passvalue):
        '''关于抵押物品的解析函数'''
        result_dict = {}
        result = []
        code_source = BeautifulSoup(response.content, 'html.parser')
        records = code_source.select("table#list")
        try:
            record = records[1]
            if record:
                person_detail = self._get_list_values([record], current_processor)

                if person_detail:
                    if len(person_detail[0]) == 4:
                        result_dict[4] = person_detail
                    elif len(person_detail[0]) == 5:
                        result_dict[5] = person_detail

                    goods = code_source.select(current_processor.get('table_selector'))
                    result_list = []
                    for t in goods:
                        try:
                            records = t.find_all('tr')
                            # 去除表头和总计表尾
                            if records:
                                if current_processor.get('table_header'):
                                    records = records[1:]
                                if current_processor.get('table_footer'):
                                    records = records[:-1]
                            for record in records:
                                r = []
                                rows = record.select('td')
                                if not rows or len(rows) == 0:
                                    continue
                                for col in rows:
                                    if col.findChildren():
                                        v = col.findChildren()[-1].string
                                        if v:
                                            r.append(v.strip())
                                        else:
                                            r.append(v)
                                    else:
                                        r.append(col.string.strip())
                                result_list.append(r)
                        except:
                            pass
                    # print('result_dict=',result_dict,'result_list=',result_list)
                    for i, j in enumerate(result_list):
                        if result_dict.get(4):
                            number_code = result_dict.get(4)[0][1]
                        elif result_dict.get(5):
                            number_code = result_dict.get(5)[0][2]

                        j.insert(0, number_code)
                        result.append(j)
        except:
            result = []
        list_infos, next_param_list = self._get_column_value_mapping(current_processor, result, passvalue)
        return list_infos

    def person_parser(self, processor_type, current_processor, response, passvalue):
        '''
        表格人员解析函数，同个表格，不同的人，结果长度不同，根据数据长度，返回需要的数据
        '''
        code_source = BeautifulSoup(response.content, 'html.parser')
        records = code_source.select("table#list")
        try:
            record = records[1]
            if record:
                person_detail = self._get_list_values([record], current_processor)
                if len(person_detail[0]) == current_processor.get("td_length"):
                    person_detail = person_detail
                else:
                    person_detail = []
        except:
            person_detail = []
        list_infos, next_param_list = self._get_column_value_mapping(current_processor, person_detail, passvalue)
        return list_infos

    def null_parser(self, _, current_processor, response, passvalue):
        self._route_many_points_many_urls(current_processor.get('detail_point'), [''], passvalue)
        return response

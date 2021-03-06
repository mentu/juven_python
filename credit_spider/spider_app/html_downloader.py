#!/usr/bin/env python
# encoding: utf-8

__author__ = 'yueyt'

from urllib.parse import urljoin, quote
import time
from config_tt import request_payload_config
import random
import os
import requests
from config_tt import base_config
from config_tt.log_config import logger
from config_tt import processor_config
from spider_app.html_parser import CreditParser
from spider_app.html_outputer import HtmlOutputer
import redis
import json
import traceback

class RedisSingleton(type):
    def __int__(self,name,bases,dict):
        super(RedisSingleton,self).__init__(name,bases,dict)
        self._instance = {}
    def __call__(self,host,port,db):
        if not self._instance.has_key((host,port,db)):
            self._instance[(host,port,db)] = super(RedisSingleton,self).__call__(host,port,db)
        return self._instance[(host,port,db)]
class RedisOp(object):
    '''
    redis的操作类，单例模式
    '''
    def __init__(self,host,port,db):
        self.host = host
        self.port = port
        self.db = db
        self.conn =redis.StrictRedis(host=self.host,port=self.port,db=self.db)
    def run_redis_fun(self,funname,*args):
        fun = getattr(self.conn,funname)
        return fun(*args)
    __metaclass__ = RedisSingleton

class HtmlDownloader(object):
    def __init__(self, queue):
        self.outputer = HtmlOutputer()
        self.s = requests.session()
        self.s.headers = base_config.request_header
        self.s.post(base_config.login_url, data=base_config.login_post_data)
        #记录登陆人行征信页面的记录，到db2表中
        os.environ['credit_status'] = '0'
        self.outputer.write_log_with_zhengxin()
        self.parser = CreditParser(queue)
        self.redis_conn = RedisOp(**base_config.redis_config)

    def _login(self):
        self.s.post(base_config.login_url, data=base_config.login_post_data)
        #记录登陆人行征信页面的记录，到db2表中
        os.environ['credit_status'] = '0'
        self.outputer.write_log_with_zhengxin()
        return self.s

    @staticmethod
    def _write_files(processor_type, response):
        import os
        import datetime

        from config_tt.base_config import basedir
        current_timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        basedir, _ = os.path.split(basedir)
        filename = os.path.join(basedir, 'html_demo', '{}.{}.html'.format(current_timestamp, processor_type))
        with open(filename, 'wb') as f:
            if response:
                f.write(response.content)

    @staticmethod
    def _get_url(current_processor, url):
        # post 的url 是配置的， get的url是从参数传递的
        url = current_processor.get('url') or url
        if not url:
            return
        try:
            # 针对url进行特殊HTML的处理
            url = url.replace(r'¤', '&curren')
            # URL 中文使用GBK编码
            url = urljoin(base_config.root_url, quote(url.encode('gbk')))
        except TypeError as e:
            logger.error('{}{}{}'.format(e.args, current_processor, url))
            return
        else:
            return url

    @staticmethod
    def _get_payload(current_processor, args):
        payload = dict(current_processor.get('payload', {}))
        if payload and isinstance(args, dict):
            for k in payload:
                if k in args:
                    payload[k] = args.get(k)
            for i in ["owesstarttime","owesstarttime1"]:
                if payload.get(i) == request_payload_config.last_quarter_start:
                    payload[i] = os.getenv('last_quarter_start')
            for i in ["owesendtime","owesendtime1","queryendtime","timepoint","queryendtime","systemDate"]:
                if payload.get(i) == request_payload_config.last_quarter_end:
                    payload[i] = os.getenv('last_quarter_end')
        if 'queryreason' in payload.keys():
            payload['queryreason'] = HtmlOutputer().get_query_reason()
        return payload

    def _get_parser_function(self, current_processor):
        parser_function = current_processor.get('parser_function')
        try:
            # 获取当前数据的解析函数
            f = getattr(self.parser, parser_function)
        except AttributeError as e:
            logger.error("i can't get parser_function,{} {}".format(__name__, current_processor))
        else:
            return f

    def _downloader(self,processor_type,request_method, url, payload, max_retry=3):
        if max_retry <= 0:
            return
        orgcode = os.getenv('orgcode')
        # 下载等待，防止被爬网站过载(可从redis中获取暂停时间)
        # delay_times = random.randint(base_config.download_delay_min, base_config.download_delay_max) or 1
        #判断当前日期是否放假,或者是否是当天禁爬时间段（晚上9:30-8:00）。
        while 1:
            holiday = self.outputer.select_spier_date()
            date = time.strftime("%Y%m%d%H",time.localtime(time.time()))
            hour = int(date[-2:])
            if holiday == '0' or hour<8 or hour >20:
                time.sleep(1800)
            else:
                break
        try:
            delay_times = self.redis_conn.run_redis_fun('hget','rh_search_date_range','delay_time')
        except:
            delay_times = False
        delay_times = float(delay_times) if delay_times else 0.2
        time.sleep(delay_times)
        # time.sleep(0.2)
        base_config.request_timeout = 70 if max_retry ==2 else 60
        base_config.request_timeout = 80 if max_retry ==1 else 60
        # 访问URL
        try:
            if request_method == 'post':
                response = self.s.post(url, data=payload, timeout=base_config.request_timeout)
            elif request_method == 'get':
                response = self.s.get(url, params=payload, timeout=base_config.request_timeout)
            else:
                return
        except Exception as e:
            logger.error(
                'request_method:{}, url:{}, times:{}, payload:{}'.format(request_method, url, max_retry, payload))
            #未能成功请求到的页面，存放到redis中处理
            # print('重试max_retry=',max_retry)
            try:
                if max_retry==1 :
                    self.redis_conn.run_redis_fun('lpush','request_url_failure_'+time.strftime('%Y%m%d',time.localtime(time.time())),
                                              json.dumps({"processor_type":processor_type,
                                                          "url":url,
                                                          "payload":payload,
                                                          'orgcode':os.getenv('orgcode'),
                                                          'last_quarter_start':os.getenv('last_quarter_start'),
                                                          'last_quarter_end':os.getenv('last_quarter_end')}))
                    self.redis_conn.run_redis_fun('expire','request_url_failure_'+time.strftime('%Y%m%d',time.localtime(time.time())),604800)
                    self.outputer.insert_data("insert into {0}.RH_ERROR_SPIDER(ORGCODE,SEARCHDATE,UPLOADTIME) values ('{1}','{2}','{3}')".format(
                                          base_config.tabschema,orgcode,
                                            os.getenv('last_quarter_end'),time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))))
                    #os.environ['credit_status'] = '1'
                    #HtmlOutputer().write_log_with_zhengxin()
                with open('error_'+time.strftime("%Y%m%d",time.localtime(time.time()))+'.log','a+') as f:
                    f.write(str(e)+'\n')
                self._login()
                response = self._downloader(processor_type,request_method, url, payload, max_retry - 1)
            except Exception as e:
                logger.error('request_method:{}, url:{}, times:{}, payload:{}'.format(request_method, url, max_retry, payload))
        if response:
            if response.status_code != 200:
                response = self._downloader(processor_type,request_method, url, payload, max_retry - 1)

        # 错误重试
        title = self.parser.get_page_title(response)
        # print("title=",title,"numbers=",max_retry)

        if title == 'failure':
            # print('内容是：',response.text)
            try:
                response = self._downloader(processor_type,request_method, url, payload, max_retry - 1)
                if max_retry==1:
                    #三次重试失败后，记录到redis中，设置key生存时间为一个星期
                    self.redis_conn.run_redis_fun('lpush','request_url_failure_'+time.strftime('%Y%m%d',time.localtime(time.time())),
                                              json.dumps({"processor_type":processor_type,
                                                          "url":url,
                                                          "payload":payload,
                                                          'orgcode':os.getenv('orgcode'),
                                                          'last_quarter_start':os.getenv('last_quarter_start'),
                                                          'last_quarter_end':os.getenv('last_quarter_end')}))
                    self.redis_conn.run_redis_fun('expire','request_url_failure_'+time.strftime('%Y%m%d',time.localtime(time.time())),604800)
                    self.outputer.insert_data(
                        "insert into {0}.RH_ERROR_SPIDER(ORGCODE,SEARCHDATE,UPLOADTIME) values ('{1}','{2}','{3}')".format(
                            base_config.tabschema, orgcode,
                            os.getenv('last_quarter_end'),
                            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))))
            except Exception as e:
                logger.error('三次重试失败后，添加错误信息到redis失败：request_method:{}, url:{}, times:{}, payload:{}'.format(request_method, url, max_retry, payload))
        if title == '企业信用信息基础数据库系统':
            self._login()
            response = self._downloader(processor_type,request_method, url, payload, max_retry - 1)
        return response

    def _get_result(self, request_method, processor_type, url, args, rsp=None):
        """获取解析后的结果，一般为json格式"""
        current_processor = processor_config.processor.get(processor_type)
        if not current_processor:
            logger.error("i can't get processor, {} {}".format(__name__, processor_type))
            return
        # 获取URL
        url = self._get_url(current_processor, url)
        # 获取payload
        payload = self._get_payload(current_processor, args)

        logger.info('http method:[{}], processor_type:[{}], url:[{}], payload:[{}]'.format(request_method, processor_type, url, payload))
        # 处理null_download时，url即为page内容的情况
        response = self._downloader(processor_type,request_method, url, payload) or rsp

        # 解析页面
        parser_function = self._get_parser_function(current_processor)
        if not parser_function:
            logger.error("i can't get parser_function, {} {}".format(__name__, processor_type))
            return
        result = parser_function(processor_type, current_processor, response, args)

        # debug
        if current_processor.get('debug'):
            self._write_files(processor_type, response)

        return result

    # post downloader
    def post_downloader(self, processor_type, url, args):
        return self._get_result('post', processor_type, url, args)

    # get downloader
    def get_downloader(self, processor_type, url, args):
        return self._get_result('get', processor_type, url, args)

    # 模拟js点击事件
    def onclick_downloader(self, processor_type, url, args):
        exec("from config_tt.processor_config import *")
        payload = eval(url)
        if not payload:
            return
        payload = dict(payload)
        if payload and isinstance(args, dict):
            payload.update(args)
        # print("onclick_downloader",payload)
        return self._get_result('post', processor_type, '', payload)

    # 空下载
    def null_downloader(self, processor_type, url, args, response):
        return self._get_result('', processor_type, url, args, response)

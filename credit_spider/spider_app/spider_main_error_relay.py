#!/usr/bin/env python
# coding: utf-8
__author__ = 'yueyt'

import datetime
from queue import Queue, Empty
import json
import os
from config_tt import base_config
from config_tt import processor_config
from spider_app.html_downloader import HtmlDownloader
from spider_app.html_outputer import HtmlOutputer
from config_tt.log_config import logger


class SpiderByQueue(object):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue
        self.download = HtmlDownloader(self.queue)
        self.output = HtmlOutputer()

    def get_processer(self, processor_type, *args):
        """
            主要处理逻辑函数，根据配置文件，获取执行逻辑处理的先后顺序
        """
        current_processor = processor_config.processor.get(processor_type)
        if not current_processor:
            logger.error("i can't found the processor, processor_type:{}, args:{}".format(processor_type, *args))
            return
        object_list = [self.download, self.output]
        for obj in object_list:
            try:
                # 根据当前的type 获取当前数据的解析函数
                f = getattr(obj, current_processor.get('function'))
            except AttributeError as e:
                pass
            else:
                # 执行当前函数并将处理结果返回，供后续处理
                # 支持多列表处理
                result = f(processor_type, *args)
                next_processor = current_processor.get('next_processor')
                if next_processor:
                    if isinstance(next_processor, str):
                        self.queue.put([next_processor, result])
                    if isinstance(next_processor, list):
                        for p in next_processor:
                            if p:
                                self.queue.put([p, result])
                break
        else:
            logger.error("i can't found the function, processor_type:{}, args:{}".format(processor_type, *args))
            return

    def run(self):
        while True:
            try:
                print("queue_size=", self.queue.qsize())
                processor_type, *args = self.queue.get(block=False)
                self.get_processer(processor_type, *args)
            except Empty:
                break

    def get_task(self):
        processor_type, *args = self.queue.get(block=False)
        self.get_processer(processor_type, *args)


def config_logger():
    # 创建一个handler，用于写入日志文件
    import datetime
    import os
    import logging
    from config_tt.base_config import basedir
    basedir, _ = os.path.split(basedir)
    current_timestamp = datetime.datetime.now().strftime('%Y%m%d')
    fh = logging.FileHandler(os.path.join(basedir, 'logs', 'spider_main.{}.log'.format(current_timestamp)),
                             encoding='utf-8')
    fh.setLevel(logging.DEBUG)

    # 再创建一个handler，用于输出到控制台
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # 定义handler的输出格式
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s][%(module)s:%(lineno)d][%(thread)d] >>> %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # 给logger添加handler
    logger.addHandler(fh)

    logger.addHandler(ch)


# Main function
if __name__ == '__main__':
    config_logger()
    import time
    target_key = 'request_url_failure_'+time.strftime('%Y%m%d',time.localtime(time.time()-24*60*60))
    # target_key = 'request_url_failure_'+time.strftime('%Y%m%d',time.localtime(time.time()))
    from spider_app.html_downloader import RedisOp
    redis_conn = RedisOp(**base_config.redis_config)
    queue_task = redis_conn.run_redis_fun('lrange',target_key,0,-1)
    try:
        for i in queue_task:
            # print(i,type(json.loads(i.decode())))
            task = json.loads(i.decode())
            if not isinstance(task,bool):
                orgcode = task.get('orgcode')
                os.environ['last_quarter_start'] = task.get('last_quarter_start')
                os.environ['last_quarter_end'] = task.get('last_quarter_end')
                # print("orgcode>>>>>>>>>>>>>>>",orgcode)
                if orgcode:
                    #判断这个企业是否正在爬取
                    spider_doing = redis_conn.run_redis_fun('sismember','rh_spider_done_orgcode',orgcode)
                    if spider_doing:
                        print("正在爬取。。。")
                        redis_conn.run_redis_fun('lpush','request_url_failure_'+time.strftime('%Y%m%d',time.localtime(time.time())),
                                                          json.dumps(task))
                        redis_conn.run_redis_fun('expire','request_url_failure_'+time.strftime('%Y%m%d',time.localtime(time.time())),604800)
                    else:
                        processor_type, *args = task.get('processor_type'),task.get('url'),task.get('payload')
                        q=Queue()
                        spider=SpiderByQueue(q)
                        spider.get_processer(processor_type, *args)
                        spider.run()
    except Exception as e:
            logger.error("重跑出错error",e)

    '''
江西赣锋锂业股份有限公司 71657512-5     3605030000000514    2016-12-01
中交第二航务工程局有限公司  17768539-1   4201010000043669    2016-12-01
贵州盛鑫矿业集团投资有限公司  56500196-7  5202010000176539   2016-12-01
临海市春风灯饰有限公司 70473721-1      3309060000195576    2016-12-01
    '''

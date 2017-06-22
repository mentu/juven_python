#!/usr/bin/env python
# coding: utf-8
__author__ = 'yueyt'

import datetime
import os
from queue import Queue, Empty
from config_tt import base_config
from config_tt import processor_config
# from config_tt import request_payload_config
from spider_app.html_downloader import HtmlDownloader
from spider_app.html_outputer import HtmlOutputer
from config_tt.log_config import logger
from spider_app.html_downloader import RedisOp


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


def start_spider(org_code):
    # queue
    url_or_data_queue = Queue()

    # 放入初始url
    #url_or_data_queue.put([base_config.start_point, '', dict(sdeporgcode=org_code)])
    url_or_data_queue.put([base_config.start_point, '', dict(loancardno=org_code)])

    spider = SpiderByQueue(url_or_data_queue)
    start_time = datetime.datetime.now()
    logger.info('{} start loancardno:{} ...'.format('-' * 80, org_code))
    spider.run()
    #爬完的企业，写入爬完企业库
    # sql = "insert into {0}.RH_CUST_QUEUE(ORG_CODE,MIDSIGNCODE,SEARCHDATE,FINISH_DATE) values ('{1}','{2}','{3}','{4}')".format(
    #     base_config.tabschema,org_code,os.getenv('midsigncode'),request_payload_config.last_quarter_end,
    #     time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())))
    # print("爬完的企业",sql)
    HtmlOutputer().update_spider_done(org_code)
    logger.info('{} end loancardno:{}, token time:{} ...'.format(
        '-' * 80, org_code, datetime.datetime.now() - start_time))


def threadpool_main():
    # task_pool = ThreadPool(base_config.concurrent_thread_amount or 10)
    # task_pool.map(start_spider, base_config.search_org_codes)
    # task_pool.close()
    # task_pool.join()
    start_spider('70469177-8')  # 爬过[70469177-8,08002456-2,78739972-0,75757833-0,74346346-0,73374565-9,]  {68268421-8,}
    '''
    江西赣锋锂业股份有限公司 71657512-5   *  欠息数据有异常
    中交第二航务工程局有限公司  17768539-1 *
    贵州盛鑫矿业集团投资有限公司  56500196-7
    临海市春风灯饰有限公司 70473721-1
    联碧德（上海）商业发展有限公司 08002456-2 3101150012118949
    '''


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
def rule_orgcode_filter(orgcode):
    """
        对需要爬取的中征码进行爬取档期的规则过滤，选择有效的时间进行爬取
    """
    date_join_dict = {'03-31':'01-01','06-30':'04-01','09-30':'07-01','12-31':'10-01'}
    redis_conn = RedisOp(**base_config.redis_config)
    #是否已经在爬取，避免同一时间爬取同一客户
    spider_doing = redis_conn.run_redis_fun('sismember','rh_spider_done_orgcode',orgcode)
    if not spider_doing:
        #加入已经爬取队列之中。防止任务重复
        redis_conn.run_redis_fun('sadd','rh_spider_done_orgcode',orgcode)
        #获取总共需要爬取的档期列表
        spider_date_list = redis_conn.run_redis_fun('smembers','rh_spider_task_period')
        for date in spider_date_list:
            date = date.decode()
            #是否已经爬取过该档期1是0否
            is_spider_done = redis_conn.run_redis_fun('sismember',date,orgcode)
            if not is_spider_done:
                print(orgcode+"的档期"+date+"正在爬取")
                os.environ['last_quarter_start'] = date[:4]+'-'+date_join_dict.get(date[-5:])
                os.environ['last_quarter_end'] = date
                start_spider(orgcode)
                redis_conn.run_redis_fun('sadd',date,orgcode)
        #爬完之后，删除正在爬取的记录
        redis_conn.run_redis_fun('srem','rh_spider_done_orgcode',orgcode)

# Main function
if __name__ == '__main__':
    config_logger()
    redis_conn = RedisOp(**base_config.redis_config)
    #从redis的队列中获取数据，首先获取优先级高的，其次是低优先级
    while 1:
        try:
            task_orgcode = redis_conn.run_redis_fun('brpop',['high_level_spider_orgcode_queue','low_level_spider_orgcode_queue'],0)
        except Exception as e:
            print(e)
        else:
            if task_orgcode:
                orgcode = task_orgcode[1].decode()
                if orgcode is None:
                    print("orgCode:",orgcode)
                    logger.error("待查询中征码为空，跳过本次查询！", orgcode)
                else:
                    os.environ['orgcode'] = orgcode
                    # os.environ['last_quarter_start'] = '2016-07-01'
                    # os.environ['last_quarter_end']= '2016-09-30'
                    rule_orgcode_filter(orgcode)
    # for i in ['71657512-5','17768539-1']:
    # import time
    # import os
    # os.environ['orgcode'] = '71657512-5'
    # starttime = time.time()
    # start_spider('55805200-2')
    # print('runtime=',time.time()-starttime)
    # time.sleep(3)
    '''
    江西赣锋锂业股份有限公司 71657512-5     3605030000000514    2016-12-01
    中交第二航务工程局有限公司  17768539-1   4201010000043669    2016-12-01
    临海市春风灯饰有限公司 70473721-1      3309060000195576    2016-12-01
    江苏颠峰投资发展有限公司  55805200-2 3205830002477022
    上海昊宇机械有限公司 13219584-X  3101240000154477
    '''

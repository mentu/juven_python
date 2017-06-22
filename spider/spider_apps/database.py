#!/usr/bin/env python
# -*- coding: utf_8 -*-

import redis
from configs import base_config


class RedisOperate(object):
    '''
    redis database
    '''
    def __init__(self):
        '''
        init redsi database
        '''
        self._redis_conn_ = redis.StrictRedis(
            host=base_config._redis_ip_,
            port=base_config._redis_port_,
            db=base_config._redis_db_)

    def _add_(self, name, value):
        '''
        add value to name
        :param name:
        :param value:
        :return:
        '''
        self._redis_conn_.sadd(name, value)

    def _sismember_(self, name, value):
        '''
        judge the value exist in name, or not
        :param name:
        :param value:
        :return:
        '''
        status = self._redis_conn_.sismember(name, value)
        return status
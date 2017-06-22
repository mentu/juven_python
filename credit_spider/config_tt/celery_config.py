#!C:\Python27\python.exe
# coding: utf-8

__author__ = 'yueyt'

# celery 任务调度
BROKER_URL = 'redis://:123456@182.119.136.140:6379/0'
CELERY_TASK_SERIALIZER = 'json'

CELERY_RESULT_BACKEND = 'redis://:123456@182.119.136.140:6379/1'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_ACCEPT_CONTENT = ['json']

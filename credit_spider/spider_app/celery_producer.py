#!C:\Python27\python.exe
# coding: utf-8

__author__ = 'yueyt'

from spider_app.celery_tasks import spider_tasks


spider_tasks.delay('74411747-1')
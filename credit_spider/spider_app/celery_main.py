#!C:\Python27\python.exe
# coding: utf-8

__author__ = 'yueyt'

from celery import Celery

app = Celery('mycelery', include=['spider_app.celery_tasks'])

app.config_from_object('config_tt.celery_config')

if __name__ == '__main__':
    app.start()

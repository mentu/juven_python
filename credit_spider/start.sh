#!/bin/bash

basedir=$HOME/credit_spider
. $basedir/venv/bin/activate

### for celery
nohup python3.5 -m spider_app.celery_main worker -l info --logfile=$basedir/logs/%n-%i.log > start.log &
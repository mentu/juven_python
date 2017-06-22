#!/bin/bash

basedir=$HOME/credit_spider
. $basedir/venv/bin/activate

nohup python3.5 -m spider_app.celery_main flower --broker=redis://182.119.136.140:6379/0 > /dev/null &
#!/bin/bash

basedir=$HOME/credit_spider
. $basedir
python3 -m spider_app.spider_error_relay > /dev/null &
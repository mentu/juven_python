# -*- coding: utf-8 -*-
import json
# Scrapy settings for landinfo project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'landinfo'

SPIDER_MODULES = ['landinfo.spiders']
NEWSPIDER_MODULE = 'landinfo.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'landinfo (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)

#--------------------- I add them -----------------------------------

CONCURRENT_REQUESTS = 100
CONCURRENT_REQUESTS_PER_DOMAIN = 30
REACTOR_THREADPOOL_MAXSIZE = 20
LOG_LEVEL = 'INFO'
COOKIES_ENABLED = False
RETRY_ENABLED = True
RETRY_TIMES = 20
REDIRECT_ENABLED = False
AJAXCRAWL_ENABLED = True
#DOWNLOAD_DELAY =  0.25

# Read from ippool.csv, convert to proper form for using. 
def get_proxies():
    inputfile = '../ippool/ippool.csv'
    file_object = open(inputfile)
    ips = file_object.read().split()[1:]
    prox = []
    for ip in ips:
        ip_dic = dict()
        ip_dic['ip_port'] = ip
        ip_dic['user_pass'] = ''
        prox += [ip_dic]
    return prox

def use_proxy():
    config_filename = 'landinfo_config.json'
    with open(config_filename, 'r') as fr:
        content_dict = json.load(fr)
    if ((content_dict[u'代理']==u'开') or (content_dict[u'代理']==u'on')):
        use = True
        print u'proxy on'
    elif ((content_dict[u'代理']==u'关') or (content_dict[u'代理']==u'off')):
        use = False
        print u'proxy off'
    else:
        print "The proxy parameter in the config file must be either 'on' or 'off' in Chinese"
        raise KeyError
    
    return use

PROXIES = get_proxies()

if use_proxy():
    DOWNLOADER_MIDDLEWARES = {
        'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 200,
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : 100,
        'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': 300,
        'landinfo.middleware.RotateUserAgentMiddleware' : 1, 
        'landinfo.middleware.ProxyMiddleware' :200,
        }
else:
    DOWNLOADER_MIDDLEWARES = {
        'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 200,
        'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware' : 100,
        'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': 300,
        'landinfo.middleware.RotateUserAgentMiddleware' : 1, 
        #'landinfo.middleware.ProxyMiddleware' :200,
        }




MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "landinfo"
MONGODB_COLLECTION = "lands"



#--------------------- I add them -----------------------------------

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'landinfo.middlewares.MyCustomSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'landinfo.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html


# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

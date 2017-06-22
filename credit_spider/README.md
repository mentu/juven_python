# credit_spider
##整体说明
本工程是异步定向爬虫框架, 爬取XX网站的相关信息，并插入mysql/db2/file中

##工程文件
* html_downloader.py
 下载器
* html_parser.py
 解析器
* html_outputer.py
 输出器
* init.sql
初始化SQL

##配置参数
* 并发线程数
concurrent_thread_amount = 3
* 爬取下载延迟
download_delay = 1
* 定向爬虫开始节点
start_point
* 查询机构代码
search_org_codes

## 使用步骤
* 执行init.sql建表
* 配置base_config.py的start_point和search_org_codes
* 运行spider_main.py: python -m spider_app.spider_main
* celery 监控命令： spider_monitor.sh
* celery worker运行命令：python3.5 -m spider_app.celery_main worker -l info





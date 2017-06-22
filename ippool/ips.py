#-*-coding:utf-8-*- 
import urllib2
import BeautifulSoup
import urllib
import socket
import csv
import json


User_Agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
header = {}
header['User-Agent'] = User_Agent


url = 'http://www.xicidaili.com/nn/'

def get_ips(target_url, url = url, pagenum=2):

    valid = [] 
    idx = 1

    # for the sake of convenience, the crawler scrapes only the first two pages. 
    
    # Or the while condition can be changed to "current number of valid IPs < number of IPs needed"
    while idx <= pagenum:

        # Adding idx is to change the current page number. 
        req_url = url + str(idx)
        
        req = urllib2.Request(req_url,headers=header)
        res = urllib2.urlopen(req).read()
        soup = BeautifulSoup.BeautifulSoup(res)
        ips = soup.findAll('tr')
        
        ip_list = [] 

        # Get all IPs on the current page. 
        for x in range(1,len(ips)):
            ip = ips[x]
            tds = ip.findAll("td")
            ip_temp = tds[1].contents[0] + ":" + tds[2].contents[0]
            ip_list += [ip_temp]
    
        
        # If no response is obtained after 5 sec, raise exception. 
        socket.setdefaulttimeout(5)
    
    
        proxys = []
        for ip in ip_list:
            proxy_host = "http://"+ ip
            proxy_temp = {"http":proxy_host}
            proxys.append(proxy_temp)
        
    
        for proxy in proxys:
            try:
                # Open target url using the IP. 
                res = urllib.urlopen(target_url,proxies=proxy).read()
                valid += [proxy['http']]
                print ">>>>>>>>>>>>>>>>>>>>>>>"
                print len(valid)
                print proxy
                # print res
            except Exception,e:
                print "<<<<<<<<<<<<<<<<<<<<<<<"
                print len(valid)
                print proxy
                print e
                continue
        idx += 1

    return valid 

config_filename = 'ips_config.json'
with open(config_filename, 'r') as fr:
    content_dict = json.load(fr)

# target_url = "http://wenshu.court.gov.cn/"
# pagenum = 5
config_filename = 'ips_config.json'
with open(config_filename, 'r') as fr:
    content_dict = json.load(fr)
target_url = content_dict[u'目标网站']
pagenum = content_dict[u'ip页数']	

ips =  get_ips(target_url = target_url, pagenum=pagenum)

# output IPs to ippool.csv
with open('ippool.csv','wb') as f:
    writer = csv.writer(f)
    writer.writerow(['ip_port'])
    for ip in ips:
        writer.writerow([ip.strip('http://').strip('\n')])
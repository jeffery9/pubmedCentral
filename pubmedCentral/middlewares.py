#from TorCtl import TorCtl, TorCtl
from scrapy import log
from scrapy.contrib.downloadermiddleware.retry import RetryMiddleware
import random
import time

class RetryChangeProxyMiddleware(RetryMiddleware):
    def _retry(self, request, reason, spider):
        log.msg('Changing proxy')
#        conn = TorCtl.connect(passphrase="1234")
#        conn.sendAndRecv('signal newnym\r\n')
#        conn.close()      
#        time.sleep(3)
        log.msg("renewed")
        
        return RetryMiddleware._retry(self, request, reason, spider)
    
 
class myProxyMiddleware(object):
    def process_request(self, request, spider):
        fd = open('proxy_list', 'r')
        proxies = fd.readlines()
        fd.close()       
        item = random.choice(proxies)
        
        arr = item.split(',')
        proxy = 'http://%s:%s' % (arr[0], arr[1].strip())
        print proxy
        
#        proxy = 'http://127.0.0.1:8123'
        request.meta['proxy'] = proxy   

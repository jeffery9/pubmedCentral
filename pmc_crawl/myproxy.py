import random
from TorCtl import TorCtl
import time
 
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

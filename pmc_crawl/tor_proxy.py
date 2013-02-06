from TorCtl import TorCtl
import time
from scrapy import log

from scrapy.contrib.downloadermiddleware.retry import RetryMiddleware

class RetryChangeProxyMiddleware(RetryMiddleware):
    def _retry(self, request, reason, spider):
        log.message('Changing proxy')
        conn = TorCtl.connect(passphrase="1234")
        conn.sendAndRecv('signal newnym\r\n')
        conn.close()      
        time.sleep(3)
        log.message("renewed")
        
        return RetryMiddleware._retry(self, request, reason, spider)

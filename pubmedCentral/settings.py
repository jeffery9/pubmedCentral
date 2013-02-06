# Scrapy settings for pubmedCentral project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'pubmedCentral'

SPIDER_MODULES = ['pubmedCentral.spiders']
NEWSPIDER_MODULE = 'pubmedCentral.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'pubmedCentral (+http://www.yourdomain.com)'


ITEM_PIPELINES = ['pubmedCentral.pipelines.PmcCrawlPipeline', ]

DOWNLOADER_MIDDLEWARES  = {                         
    'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    'pubmedCentral.middlewares.myProxyMiddleware': 100,
#    'pubmedCentral.middlewares.RetryChangeProxyMiddleware': 600,
    
     }

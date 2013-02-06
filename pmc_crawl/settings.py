# Scrapy settings for pmc_crawl project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/topics/settings.html
#

BOT_NAME = 'pmc_crawl'

SPIDER_MODULES = ['pmc_crawl.spiders']
NEWSPIDER_MODULE = 'pmc_crawl.spiders'

ITEM_PIPELINES = ['pmc_crawl.pipelines.PmcCrawlPipeline', ]

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'pmc_crawl (+http://www.yourdomain.com)'

DOWNLOADER_MIDDLEWARE = {
#     'pmc_crawl.tor_proxy.RetryChangeProxyMiddleware': 600,
     'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 110,
    'pmc_crawl.myproxy.myProxyMiddleware': 100,
     }

from scrapy.selector import HtmlXPathSelector
from pubmedCentral.items import PubmedcentralItem
from scrapy.spider import BaseSpider
from scrapy.contrib.downloadermiddleware.retry import RetryMiddleware

class PmcSpider(BaseSpider):    
    user_agent ='Mozilla/6.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1'
    name = 'pmc'
    allowed_domains = ['www.ncbi.nlm.nih.gov']
    urls =[]
    fd = open('links')
    for url in fd:
        urls.append(url.strip())   
        
    start_urls = tuple(urls)
    
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        status = response.status
        url = response.url
        
        if status ==  200 :         
            item = PubmedcentralItem() 
            item['url'] = response.url             
            item['title'] = hxs.select('//*[@class="content-title"]').extract()
            item['authors'] = hxs.select('//*[@class="contrib-group fm-author"]').extract() 
            item['contacts'] = hxs.select('//*[@class="fm-authors-info fm-panel hide half_rhythm"]').extract()     
            item['abstract'] = hxs.select('//*[@id="maincontent"]/div[1]/div[3]/div/div[3]').extract()
            item['keywords'] = hxs.select('//*[@class|id="kwd-text"]').extract()
            item['publication'] = hxs.select('//*[@id="maincontent"]/div[1]/div[3]/div/div[1]/div[1]/div/div[1]/div/div[1]').extract()
            
            yield item     
                
        else:
            
            yield Request(url, self.parse)  
                   
            
        
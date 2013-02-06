from pmc_crawl.items import PmcCrawlItem
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http.request import Request
from scrapy.selector import HtmlXPathSelector, HtmlXPathSelector
from scrapy.spider import BaseSpider
from selenium import selenium
import time
import lxml.html
from lxml import etree

class PmcSpider(BaseSpider):
    name = 'pmc'
    user_agent ='Mozilla/6.0 (Windows NT 6.2; WOW64; rv:16.0.1) Gecko/20121011 Firefox/16.0.1'
    allowed_domains = ['www.ncbi.nlm.nih.gov']
    
    start_urls = ['http://www.ncbi.nlm.nih.gov/pmc/?term=((china%5BAffiliation%5D)+OR+chinese%5BAffiliation%5D)+AND+(%222000%22%5BPublication+Date%5D+%3A+%223000%22%5BPublication+Date%5D)']  
    
    def __init__(self, **kwargs):
        print kwargs
        self.selenium = selenium("10.10.103.6", 4444, "*firefox", "http://www.ncbi.nlm.nih.gov")
        self.selenium.start()    
    
    def __del__(self):
        self.selenium.stop()
                
    def parse(self, response):      
        base_url = 'http://www.ncbi.nlm.nih.gov'
           
        sel = self.selenium
        sel.open(response.url) 
        
        sel.click("link=Display Settings:")
        sel.click("id=ps100")
        sel.click("//div[@id='display_settings_menu']/fieldset[2]/ul/li[5]/label")
        sel.click("name=EntrezSystem2.PEntrez.Pmc.Pmc_ResultsPanel.Pmc_DisplayBar.SetDisplay")
        sel.wait_for_page_to_load("30000")
        html = sel.get_html_source()
        root = lxml.html.fromstring(html)
        links = root.xpath('//*[@class="title"]/a/@href') 
        pages = root.xpath('//*[@class="num"]/@last')[0]
        current = root.xpath('//*[@class="num"]/@value')[0]
                 
        hrefs = []
#                
#        hxs = HtmlXPathSelector(response)        
#        links = hxs.select('//*[@class="title"]/a/@href').extract()  
        hrefs.extend(links)
#        pages = hxs.select('//*[@class="num"]/@last').extract()[0]
                
        count = 0
        print count , current, pages   
        print len(hrefs)
        
        while int(current) < int(pages): 
            count = count + 1            
            print '....\n'
            print count , current, pages           
            
            try:                    
                sel.click("link=Next >")
                sel.wait_for_page_to_load("30000")
                html = sel.get_html_source()
                root = lxml.html.fromstring(html)            
                links = root.xpath('//*[@class="title"]/a/@href')
                current = root.xpath('//*[@class="num"]/@value')[0]
                hrefs.extend(links)
                print len(hrefs)
                
            except Exception as ex:
                print ex     
        
        file = open('links','wb')              
        
        for href in hrefs: 
            url = base_url + href    
            file.write(url + '\n')        
            yield Request(url, self.parse_publication)  
            time.sleep(10)    
        
        file.close()    
        
    def parse_publication(self, response):        
        status = response.status
        url = response.url
        
        if status ==  200 :  
            hxs = HtmlXPathSelector(response)
            item = PmcCrawlItem() 
            item['url'] = response.url             
            item['title'] = hxs.select('//*[@class="content-title"]').extract()
            item['authors'] = hxs.select('//*[@class="contrib-group fm-author"]').extract() 
            item['contacts'] = hxs.select('//*[@class="fm-authors-info fm-panel hide half_rhythm"]').extract()     
            item['abstract'] = hxs.select('//*[@id="maincontent"]/div[1]/div[3]/div/div[3]').extract()
            item['keywords'] = hxs.select('//*[@class|id="kwd-text"]').extract()
            item['publication'] = hxs.select('//*[@id="maincontent"]/div[1]/div[3]/div/div[1]/div[1]/div/div[1]/div/div[1]').extract()
            
            yield item
            
        else:            
            yield Request(url, self.parse_publication)  
                   
            

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class PmcCrawlItem(Item):
    # define the fields for your item here like:
    # name = Field()
    url = Field()
    title = Field()
    authors = Field()
    contacts = Field()
    abstract = Field()
    keywords = Field()
    publication = Field()
    
    def __str__(self):
        pass
#        
#        return '\n titile : %s ,\n authors: %s ,\n abstract : %s ,\n keywords: %s ,\n publication: %s'\
#            % (self.get('title'), self.get('authors'), self.get('abstract'), self.get('keywords'), self.get('publication'))
#         

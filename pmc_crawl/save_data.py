# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import lxml.html
import simplejson as json
from lxml.html.clean import Cleaner
import pickle

class save_data(object):
    
    def __init__(self):
        self.file = codecs.open('items.txt', 'w', 'utf-8')
        
    def __del__(self):
        self.file.close()
    
    def process_item(self, item, spider):        
        
        """
        url = Field()
        title = Field()
        authors = Field()
        contacts = Field()
        abstract = Field()
        keywords = Field()
        publication = Field()
        
        """

        

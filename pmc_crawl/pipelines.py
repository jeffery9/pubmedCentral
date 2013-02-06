# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/topics/item-pipeline.html

import lxml.html
import simplejson as json
from lxml.html.clean import Cleaner
import codecs
import pickle
import datetime

class PmcCrawlPipeline(object):
    
    def __init__(self):
        now = datetime.datetime.now()
        result = 'result_' + str(now)
        datafile = 'datafile_' + str(now)
        self.file = codecs.open(result, 'w', 'utf-8')
        self.pfile = open(datafile, 'wb')
        self.dataset = []
        
    def __del__(self):
        self.file.close()
        self.pfile.close()
    
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
        publication = item['publication']
        authors = item['authors']
        contacts = item['contacts']
        url = item['url']
        titile = item['title']
        abstract = item['abstract']
        keywords = item['keywords']
              
#        cleaner = Cleaner(remove_tags=['em', 'a'])
        
        titile = lxml.html.fromstring(titile[0])
#        titile = cleaner.clean_html(titile)
        titile = ' '.join([tx.replace('\n', ' ').strip() for tx in titile.itertext() ])        
        
        abstract = lxml.html.fromstring(abstract[0])
#        abstract = cleaner.clean_html(abstract)
        abstract = ' '.join([tx.strip() for tx in abstract.itertext() ])    
        
        kw_list = []               
        if len(keywords) > 0:
            for kw in keywords:                
                html = lxml.html.fromstring(kw)                                               
                kws = "".join([it.lstrip() for it in html.itertext()])
                kws_list = kws.split(",")
                kw_list.extend(kws_list)
        
        kws_list = []
        for it in kw_list:
            new = it.strip()
            kws_list.append(new)
               
        data = {}
        data['url'] = url
        data['titile'] = titile
        data['abstract'] = abstract
        data['keywords'] = kws_list              
        
        etree_publication = lxml.html.fromstring(publication[0])
        
        spans = etree_publication.cssselect('span')
        publicaiton_dict = {}
        for span in spans: publicaiton_dict[span.get('class')] = span.text_content().strip(';,(): ')
        
        data['publicaiton'] = publicaiton_dict
        
        ret = authors[0].split("<a")

        del ret[0]
        del ret[-1]
        
        authors_dict = {}
        for element in ret:
            element = "<a" + element    
            html = lxml.html.fromstring(element)
            asel = html.cssselect('a')  
            key = asel[0].text_content().format()    
            sup = html.cssselect('sup')
            value = []
            for ele in  sup:
                val = ele.text_content().strip(',').format()
                value.append(val)
            
            authors_dict[key] = value

        html = lxml.html.fromstring(contacts[0]) 
        email_addr = []                               
        post = {}
        div = html.cssselect('div.fm-affl')
        count = 0
        for el in div: 
            a = el.cssselect('a')              
            for b in a:  
                email_addr.append(b.text_content().format())
                
            if el.find('sup') is not None:
                for val in el.xpath('sup'):
                    key = val.text_content().format()
                    el.find('sup').drop_tree()
            else:
                key = 'x_' + str(count)
                count = count + 1
                    
            post[key] = el.text_content().format()
            
        mail_post = {}
        
        for author in authors_dict.iterkeys():            
            post_addr = []            
            sups = authors_dict[author]            
            if sups is not None:                
                for sup in sups:                              
                    if post.has_key(sup) :  post_addr.append(post[sup])            
            for a in post.iterkeys():
                if a.find('x_') == -1:  pass
                else:
                    post_addr.append(post[a])  
                          
            mail_post[author] = post_addr              
        
        data['posts'] = mail_post
        
        try:
            scripts = html.cssselect('script')
            for script in scripts : 
                text = script.getprevious()
                email = text.text_content().format()               
                email_addr.append(email)    
     
        except Exception as ex:
            print ex        
               
        email_addr_0 = []               
        for addr in email_addr: 
            new = addr.replace("/at/", "@")
            email_addr_0.append(new)
        
        data['emails'] = email_addr_0

        print json.dumps(data , sort_keys=True, indent=4)
        
        self.file.write(' "%s" \t' % unicode(data['titile']))
        self.file.write(' "%s" \t' % unicode(data['keywords']))
        self.file.write(' "%s" \t' % unicode(data['emails']))
        self.file.write(' "%s" \t' % unicode(data['url']))     
        self.file.write(' "%s" \t' % unicode(data['publicaiton']['citation-abbreviation']))
        self.file.write('\n')
        
        self.dataset.append(data)
                
        return item 

    def close_spider(self, spider):
        pickle.dump(self.dataset, self.pfile)

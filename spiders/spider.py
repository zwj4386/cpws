import scrapy
import pymysql
from scrapy.http import Request
from scrapy.selector import Selector
from cpws.items import CpwsItem
import sys
reload(sys)
import os
sys.setdefaultencoding('utf-8')
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

class Spider(scrapy.Spider):
    name = 'cpws'
    start_urls = [
        #'http://openlaw.cn/search/judgement/type?causeId=08df5355fffa4053b9f4478a46cd51d2',
        #'http://openlaw.cn/search/judgement/type?causeId=44f522e92013462abc4ad7049ebd9e3e',
        #'http://openlaw.cn/search/judgement/type?causeId=d8347b89678645e1887045b4200e822f',
        #'http://openlaw.cn/search/judgement/type?litigationType=Criminal',
        #'http://openlaw.cn/search/judgement/type?litigationType=Administration'
        'http://www.baidu.com'
    ]
    allowed_domain = ['openlaw.cn']

def parse(self,response):
    try:
        hx = Selector(response)
        urlList = hx.xpath('//h3[@class="entry-title"]/a/@href').extract()
        for i in urlList:
            print(i)
            url = ''.join(i)
            yield Request(url,
                          headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'},
                          callback= self.getItem)
    except Exception,e:
        print(e)

def getItem(self,response):
    try:
        item = CpwsItem()
        ch = Selector(response)
        item['name'] = ch.xpath('//h2[@class="entry-title"]/text()').extract_first()
        item['date'] = ch.xpath('//li[@class="ht-kb-em-date"]/text()').extract_first()
        item['court'] =ch.xpath('//li[@class="ht-kb-em-author"]/a/text()').extract_first()
        item['casenu'] = ch.xpath('//li[@class="ht-kb-em-category"]/text()').extract_first()
        item['ltg'] = ch.xpath('//div[@id="Litigants"]/p/text()').extract_first()
        content = ch.xpath('//div[@class="part"]/p')
        item['content'] = content.xpath('string(.)').extract_first()
        yield item
    except Exception,e:
        print(e)
# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from scrapy.http import Request
import re,os
class BiqugeSpider(scrapy.Spider):
    name = 'biquge'
    allowed_domains = ['www.biquge.com.tw']
    start_urls = ['http://www.biquge.com.tw/15_15558/']
    
    def parse(self, response):
        list_urls = response.xpath('//div[@id="list"]/dl/dd/a/@href').extract()
        self.bookname = response.xpath('//div[@id="info"]/h1/text()').extract_first()
        for list_url in list_urls:
            yield Request(url=parse.urljoin(response.url, list_url), callback=self.parse_detail)

    def parse_detail(self, response):
        title = response.xpath('//div[@class="bookname"]/h1/text()').extract_first()
        content = response.xpath('//div[@id="content"]').extract_first()
        content = re.search('.*?content">(.*?)</div>',content,re.S)
        content = re.sub(r'<br>','',content.group(1))
        with open('E:\\VS code\\python\\file\小说\\'+self.bookname+'.txt','a',encoding='utf-8') as f:
            f.write(title+'\n'+content+'\n')
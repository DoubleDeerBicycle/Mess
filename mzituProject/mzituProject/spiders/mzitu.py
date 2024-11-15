# -*- coding: utf-8 -*-
import scrapy
from mzituProject.items import MzituprojectItem
from time import sleep
class MzituSpider(scrapy.Spider):
    name = 'mzitu'
    allowed_domains = ['www.mzitu.com']
    start_urls = ['http://www.mzitu.com/tag/xiuren//']

    def parse(self, response):
        uls = response.css('#pins li')
        for ul in uls:
            item = MzituprojectItem()
            url = ul.css('a::attr(href)').extract_first()
            title = ul.css('a img::attr(alt)').extract_first()
            date = ul.css('.time::text').extract_first()
            number = ul.css('.view::text').extract_first()
            
            item['url'] = url
            item['title'] = title
            item['date'] = date
            item['number'] = number
            yield item
        
        next = response.css('.next::attr(href)').extract_first()
        url = response.urljoin(next)
        yield scrapy.Request(url=url, callback=self.parse)


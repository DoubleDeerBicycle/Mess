# -*- coding: utf-8 -*-
import scrapy


class MmjpgSpider(scrapy.Spider):
    name = 'mmjpg'
    allowed_domains = ['www.mmjpg.com']
    start_urls = ['http://www.mmjpg.com/']

    def parse(self, response):
        pass

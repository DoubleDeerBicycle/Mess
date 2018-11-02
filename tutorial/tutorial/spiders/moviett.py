# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
from scrapy.http import Request
from tutorial.items import MoviettItem
from scrapy.loader import ItemLoader
import re
class MovietSpider(scrapy.Spider):
    name = 'moviett'
    allowed_domains = ['www.ygdy8.net']
    start_urls = ['http://www.ygdy8.net/html/gndy/dyzz/index.html']

    def parse(self, response):
        #获取当前页下所有movie的链接
        movie_urls = response.css('.co_content8 .ulink::attr(href)').extract()
        #遍历后回调给parse_detail处理
        for movie_url in movie_urls:
            yield Request(url=parse.urljoin(response.url, movie_url),callback=self.parse_detail)
        
        #获取下一页
        page_num = int(re.search('.*?共(\d+)页',response.text,re.S).group(1))
        for num in range(2,page_num+1):
            yield Request(url='http://www.ygdy8.net/html/gndy/dyzz/list_23_'+str(num)+'.html',callback=self.parse)


    def parse_detail(self, response):
        #通过itemloder加载item
        item_loder = ItemLoader(item=MoviettItem(), response=response)
        item_loder.add_css('url', '#Zoom td > a::text')
        item_loder.add_css('movie_name', '.title_all > h1 > font::text')
        item = item_loder.load_item()

        yield item
# -*- coding: utf-8 -*-
import scrapy
import re
import os

class MaomiSpider(scrapy.Spider):
    name = 'maomi'
    allowed_domains = ['www.978ii.com', '991video.com']
    start_urls = ['https://www.978ii.com/shipin/list-%E7%9F%AD%E8%A7%86%E9%A2%91.html']
    
    def parse(self, response):
        urls = response.css('.grid.effect-1 li a::attr(href)').extract()
        names = response.css('.grid.effect-1 li a::attr(title)').extract()
        for url, name in zip(urls, names):
            yield scrapy.Request(url=response.urljoin(url), meta={'name':name}, callback=self.parse_video)

        next_page = response.xpath('//a[contains(@title, "下一页")]/@href').extract_first()
        if next_page:
            yield scrapy.Request(url=response.urljoin(next_page), callback=self.parse)

    def parse_video(self, response):
        video_url = re.sub('one\.', '' ,response.css('#lin1k0::attr(data-clipboard-text)').extract_first())
        name = re.sub('[ \/:*?"<>|\r".\n]', '', response.meta.get('name'))
        #视频存放目录
        path_dir = os.path.dirname(os.getcwd())+'/file/视频/猫咪/'
        #判断视频存放目录是否存在
        if not os.path.exists(path_dir):
            os.makedirs(path_dir)
        path = path_dir+name+'.mp4'
        if not os.path.exists(path):
            yield scrapy.Request(url=video_url, meta={'path': path, 'name': name}, callback=self.parse_down)

    def parse_down(self, response):
        with open(response.meta.get('path'), 'wb') as f:
            print('download:'+response.meta.get('name'))
            f.write(response.body)
            f.close()

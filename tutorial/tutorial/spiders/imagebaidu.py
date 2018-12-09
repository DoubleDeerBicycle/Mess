# -*- coding: utf-8 -*-
import scrapy
import time
from urllib.parse import urlencode
import json
from tutorial.items import ImagebaiduItems
from scrapy.loader import ItemLoader


class ImagebaiduSpider(scrapy.Spider):
    name = 'imagebaidu'
    allowed_domains = ['image.baidu.com']
    start_urls = ['http://image.baidu.com/']
    # 定义请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3371.0 Safari/537.36'
    }
    # 图片关键词
    image = '门匾素材'
    url = 'https://image.baidu.com/search/acjson?'
    # 页数（每页默认30张图片）
    page = 5 
    def parse(self, response):
        for num in range(self.page*3):
            if num % 3 == 0:
                num = num*10
                data = {
                    'tn': 'resultjson_com',
                    'ipn': 'rj',
                    'ct': '201326592',
                    'is': '',
                    'fp': 'result',
                    'queryWord': self.image,
                    'cl': '2',
                    'lm': '-1',
                    'ie': 'utf-8',
                    'oe': 'utf-8',
                    'adpicid': '',
                    'st': '-1',
                    'z': '',
                    'ic': '0',
                    'hd': '' ,
                    'latest': '',
                    'copyright': '',
                    'word': self.image,
                    's': '',
                    'se': '',
                    'tab': '',
                    'width': '',
                    'height': '',
                    'face': '0',
                    'istype': '2',
                    'qc': '',
                    'nc': '1',
                    'fr': '',
                    'expermode': '',
                    'selected_tags': '',
                    'pn': num,
                    'rn': '30',
                    'gsm': '1e',
                    '1543718075201': ''
                }
                newurl = self.url+urlencode(data)
                yield scrapy.Request(newurl, headers=self.headers, callback=self.parse_image)

    def parse_image(self, response):
        image_item = ItemLoader(item=ImagebaiduItems(), response=response)
        result = json.loads(response.text)

        urls = []
        for data in result.get('data'):
            if 'thumbURL' in data.keys():
                urls.append(data.get('thumbURL'))
        image_item.add_value('image_url', urls)
        item = image_item.load_item()
        yield item
            
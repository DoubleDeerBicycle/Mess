import requests
import os
import re
from scrapy.selector import Selector
from urllib.parse import urljoin


class Font():
    def __init__(self):
        self._url = 'http://font.knowsky.com/'

    def _rq_index(self):
        try:
            response = requests.get(self._url)
            if response.status_code == 200:
                response.encoding = 'utf-8'
                doc = Selector(text=response.text)
                return doc
            else:
                return None
        except Exception as e:
            return None
            print(e)

    def _get_data(self):
        doc = self._rq_index()
        names = doc.css('.fontpic a::attr(title)').extract()
        urls = doc.css('.fontpic a::attr(href)').extract()
        images = doc.css('.fontpic a img::attr(src)').extract()
        for name,url,image in zip(names,urls,images):
            yield{
                'name': name,
                'url': urljoin(self._url, url),
                'image': image
            }

    def down_data(self):
        for datas in self._get_data():
            print(datas.get('name'))
            print(datas.get('url'))
            print(datas.get('image'))
        
font = Font()
font.down_data()
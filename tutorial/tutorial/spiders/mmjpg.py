# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
import os,re,requests
from hashlib import md5
import random
class MmjpgSpider(scrapy.Spider):
    name = 'mmjpg'
    allowed_domains = ['www.mmjpg.com']
    start_urls = ['http://www.mmjpg.com/']

    # 数据存放路径
    file_path = 'file/图片/'
    
    def parse(self, response):
        # 获取当前页所有的图片集
        images = response.css('.pic ul li a::attr(href)').extract()
        
        for image in images:
            yield scrapy.Request(url=image, callback=self.parse_image)

        # 下一页
        count_page = response.css('.page .info::text').extract_first()
        re_count_page = re.search('.*?(\d+).*?', count_page).group(1)
        for page in range(2, int(re_count_page)+1):
            next = 'http://www.mmjpg.com/home/{page}'.format(page=page)  
            yield scrapy.Request(url=next, callback=self.parse, priority=5)

    # 爬取图片集链接
    def parse_image(self, response):
        name = response.css('.article h2::text').extract_first()
        name = re.sub('\(|\d|\)| ', '', name)
        image_url = response.css('#content a img::attr(src)').extract_first()
        code = ''
        for i in range(5):
            a = chr(random.randint(97, 122))
            b = random.randint(1, 9)
            uuid = random.choice([a, b])
            code += str(uuid)
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KGTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Content-Type':'image/jpeg',
            'Gost':'img.mmjpg.com',
            'Referer': response.url,
            'If-None-Match':'59a96b74-%s'%code,
            }
        content = requests.get(image_url, headers=headers).content

        dir_path = self.file_path+name
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        path = self.file_path+name+'/'+md5(content).hexdigest() +'.jpg'
        with open(path, 'wb') as f:
            f.write(content)

        next = response.css('.page .next::attr(href)').extract_first()
        page = response.urljoin(next)
        yield scrapy.Request(url=page, callback=self.parse_image, priority=10)
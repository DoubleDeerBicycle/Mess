# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
from tutorial.items import JobboleItem
from tutorial.utils.common import get_md5
import datetime
class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        #获取文章列表页中的文章url
        post_nodes = response.css('#archive .post .post-thumb a')
        for post_node in post_nodes:
            post_url = post_node.css('::attr(href)').extract_first()
            post_image_url = post_node.css('img::attr(src)').extract_first()
            yield Request(url=parse.urljoin(response.url,post_url),meta={'post_image_url':parse.urljoin(response.url, post_image_url)}, callback=self.parse_detail)
        
        #提取下一页url
        #response.xpath('//a[contains(@class,"next")]/@href').extract_first()
        next_url = response.css('.next::attr(href)').extract_first()
        if next_url:
            yield Request(url=parse.urljoin(response.url,next_url),callback=self.parse)

    def parse_detail(self, response):
        item = JobboleItem()
        #通过xpath提取数据
        # title = response.xpath('//div[@class="entry-header"]/h1/text()')
        # date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]').re('.*?(\d{4}/\d{1,2}/\d{1,2})')[0]
        # praise_nums = response.xpath('//div[@class="post-adds"]/span[1]').re('.*?">(\d)</h10>(.*?)</span>')[0]+response.xpath('//div[@class="post-adds"]/span[1]').re('.*?">(\d+)</h10>(.*?)</span>')[1]
        # collection_nums = response.xpath('//div[@class="post-adds"]/span[2]/text()').extract_first().replace('  ','0')
        # comments_nums = response.xpath('//div[@class="post-adds"]/a[1]/span[1]/text()').extract_first()
        # content = response.xpath('//div[@class="entry"]').extract()
        
        #通过css提取数据
        post_image_url = response.meta.get('post_image_url')
        title = response.css('div.entry-header > h1::text').extract_first()
        date = response.css('p.entry-meta-hide-on-mobile::text').re('.*?(\d{4}/\d{1,2}/\d{1,2})')[0]
        praise_nums = response.css('div.post-adds .btn-bluet-bigger > h10 ::text').extract_first()
        collection_nums = response.css('div.post-adds span:nth-child(2)::text').re('.*?(\d+)')
        comments_nums = response.css('div.post-adds >a > span::text').re('.*?(\d+)')
        content = response.css('div.entry').extract_first()

        if not praise_nums:
            praise_nums = 0
        else:
            praise_nums = int(praise_nums)
        if not comments_nums:
            comments_nums = 0
        else:
            comments_nums = int(comments_nums[0])
        if not collection_nums:
            collection_nums = 0
        else:
            collection_nums = int(collection_nums[0])
            
        try:
            date = datetime.datetime.strptime(date,'%Y/%m/%d').date()
        except Exception as e:
            date = datetime.datetime.now()
        item['url_object_id'] = get_md5(response.url)
        item['title'] = title
        item['url'] = response.url
        item['date'] = date
        item['content'] = content
        item['praise_nums'] = praise_nums
        item['collection_nums'] = collection_nums
        item['comments_nums'] = comments_nums
        item['post_image_url'] = [post_image_url]
        item['post_image_path'] = None
        yield item
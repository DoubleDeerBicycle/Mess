# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class JobboleItem(scrapy.Item):
    title = scrapy.Field()
    date = scrapy.Field()
    praise_nums = scrapy.Field()
    collection_nums = scrapy.Field()
    comments_nums = scrapy.Field()
    content = scrapy.Field()
    post_image_url = scrapy.Field()
    post_image_path = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
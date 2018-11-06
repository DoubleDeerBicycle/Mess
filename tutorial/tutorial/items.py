# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst
import datetime,re
class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


#解析日期
def date_convert(value):
    try:
        date = datetime.datetime.strftime(value, '%Y/%m/%d').date()
    except Exception as e:
        date = datetime.datetime.now().date()

    return date


def praise_nums_convert(value):
    if not value:
        praise_nums = 0
    else:
        value = re.search('(\d)', value).group(1)
        praise_nums = int(value)

    return praise_nums


def comments_nums_convert(value):
    if not value:
        comments_nums = 0
    else:
        value = re.search('(\d)', value).group(1)
        comments_nums = int(value)

    return comments_nums


def collection_nums_convert(value):
    if not value:
        collection_nums = 0
    else:
        value = re.search('(\d)', value).group(1)
        collection_nums = int(value)

    return collection_nums


class JobboleItem(scrapy.Item):
    title = scrapy.Field(
        #只取列表中的一个值
        output_processor=TakeFirst()
    )
    date = scrapy.Field(
        #调用方法对参数进行清洗
        input_processor = MapCompose(date_convert),
        output_processor = TakeFirst()
    )
    praise_nums = scrapy.Field(
        input_processor = MapCompose(praise_nums_convert),
        output_processor = TakeFirst()
    )
    collection_nums = scrapy.Field(
        input_processor = MapCompose(collection_nums_convert),
        output_processor = TakeFirst()
    )
    comments_nums = scrapy.Field(
        input_processor = MapCompose(comments_nums_convert),
        output_processor = TakeFirst()
    )
    content = scrapy.Field(
        output_processor = TakeFirst()
    )
    post_image_url = scrapy.Field(
        output_processor = TakeFirst()
    )
    post_image_path = scrapy.Field(
        output_processor = TakeFirst()
    )
    url = scrapy.Field(
        output_processor = TakeFirst()
    )
    url_object_id = scrapy.Field(
        output_processor = TakeFirst()
    )


class MoviettItem(scrapy.Item):
    url = scrapy.Field(
        output_processor = TakeFirst()
    )

    movie_name = scrapy.Field(
        output_processor = TakeFirst()
    )


#知乎问题item
class ZhihuQuestionItem(scrapy.Item):
    zhihu_id = scrapy.Field()

    topics = scrapy.Field()

    url = scrapy.Field()

    title = scrapy.Field()

    content = scrapy.Field()

    answer_num = scrapy.Field()

    comments_num = scrapy.Field()

    follower_user_num = scrapy.Field()

    visit_num = scrapy.Field()

    crawl_time = scrapy.Field()

#知乎的回答item
class ZhihuAnswerItem(scrapy.Item):
    zhihu_id = scrapy.Field()

    url = scrapy.Field()

    question_id = scrapy.Field()

    author_id = scrapy.Field()

    content = scrapy.Field()

    parise_num = scrapy.Field()

    comments_num = scrapy.Field()

    create_time = scrapy.Field()

    update_time = scrapy.Field()

    crawl_time = scrapy.Field()
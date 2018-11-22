# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join
import datetime,re
from w3lib.html import remove_tags


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

    def get_insert_sql(self):
        insert_sql = '''
                   insert into jobbole(title, url, date, praise_nums, collection_nums, comments_nums, content, post_image_url, post_image_path ,url_object_id)
                   values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
               '''
        params = (self['title'], self['url'], self['date'], self['praise_nums'], self['collection_nums'], self['comments_nums'],
                               self['content'], self['post_image_url'], self['post_image_path'], self['url_object_id'],)
        return insert_sql, params


class MoviettItem(scrapy.Item):
    url = scrapy.Field(
        output_processor = TakeFirst()
    )

    movie_name = scrapy.Field(
        output_processor = TakeFirst()
    )

    def get_insert_sql(self):
        insert_sql = '''
                                   insert into moviett(url,movie_name)
                                   values (%s, %s)
                               '''
        params = (self['url'], self['movie_name'])
        return insert_sql, params


#   知乎问题item
class ZhihuQuestionItem(scrapy.Item):
    zhihu_id = scrapy.Field(
        output_processor=TakeFirst()
    )

    topics = scrapy.Field(
        output_processor=TakeFirst()
    )

    url = scrapy.Field(
        output_processor=TakeFirst()
    )

    title = scrapy.Field(
        output_processor=TakeFirst()
    )

    content = scrapy.Field(
        output_processor=TakeFirst()
    )

    answer_num = scrapy.Field(
        output_processor=TakeFirst()
    )

    comments_num = scrapy.Field(
        output_processor=TakeFirst()
    )

    follower_user_num = scrapy.Field(
        output_processor=TakeFirst()
    )

    visit_num = scrapy.Field(
        output_processor=TakeFirst()
    )

    crawl_time = scrapy.Field(
        output_processor=TakeFirst()
    )

    def get_insert_sql(self):
        #   插入知乎question的sql语句
        insert_sql = '''
            insert into zhihu_question(zhihu_id,topics,url,title,content,answer_num,comments_num,follower_user_num,
            visit_num,crawl_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON DUPLICATE KEY UPDATE content=VALUES(content),comments_num=VALUES(comments_num),
            answer_num=VALUES(answer_num),follower_user_num=VALUES(follower_user_num) 
        '''
        params = (self['zhihu_id'], self['topics'],self['url'], self['title'],self['content'], self['answer_num'],
                  self['comments_num'], self['follower_user_num'],self['visit_num'], self['crawl_time'])

        return insert_sql, params


#   知乎的回答item
class ZhihuAnswerItem(scrapy.Item):
    zhihu_id = scrapy.Field(
        output_processor=TakeFirst()
    )

    title = scrapy.Field(
        output_processor=TakeFirst()
    )

    headline = scrapy.Field(
        output_processor=TakeFirst()
    )

    user_name = scrapy.Field(
        output_processor=TakeFirst()
    )
    url = scrapy.Field(
        output_processor=TakeFirst()
    )

    question_id = scrapy.Field(
        output_processor=TakeFirst()
    )

    author_id = scrapy.Field(
        output_processor=TakeFirst()
    )

    content = scrapy.Field(
        output_processor=TakeFirst()
    )

    praise_num = scrapy.Field(
        output_processor=TakeFirst()
    )

    comments_num = scrapy.Field(
        output_processor=TakeFirst()
    )

    create_time = scrapy.Field(
        output_processor=TakeFirst()
    )

    update_time = scrapy.Field(
        output_processor=TakeFirst()
    )

    crawl_time = scrapy.Field(
        output_processor=TakeFirst()
    )

    def get_insert_sql(self):
        #   插入知乎AnswerItem的sql语句
        insert_sql = '''
            insert into zhihu_answer(zhihu_id,url,question_id,author_id,content,praise_num,comments_num,create_time,
            update_time,crawl_time,title,headline,user_name) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON DUPLICATE KEY UPDATE content=VALUES(content),praise_num=
            VALUES(praise_num),comments_num=VALUES(comments_num),update_time=VALUES(update_time)
        '''
        params = (self['zhihu_id'], self['url'],self['question_id'], self['author_id'],self['content'], self['praise_num'],
                  self['comments_num'], self['create_time'],self['update_time'], self['crawl_time'], self['title'],self['headline'], self['user_name'])

        return insert_sql, params


    #拉钩

def remove_splash(value):
    return value.replace('/', '')

def re_enter(value):
    return re.sub('\\n| |查看地图', '', value)

def remove_null(value):
    end = value.rfind(' ')
    if end == -1:
        return value
    return value[0:end-1]


class LagouItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class LagouItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    job_desc = scrapy.Field(
        input_processor=MapCompose(remove_tags)
    )
    job_advantage = scrapy.Field()
    tags = scrapy.Field(
        input_processor=Join(',')
    )
    crawl_time = scrapy.Field()
    company_name = scrapy.Field()
    company_url = scrapy.Field()
    job_addr = scrapy.Field(
        input_processor=MapCompose(remove_tags, re_enter)
    )
    pulish_time = scrapy.Field(
        input_processor=MapCompose(remove_null)
    )
    job_type = scrapy.Field()
    degree_need = scrapy.Field(
        input_processor=MapCompose(remove_splash)
    )
    work_years = scrapy.Field(
        input_processor=MapCompose(remove_splash)
    )
    job_city = scrapy.Field(
        input_processor=MapCompose(remove_splash)
    )
    salary_min = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = '''
            insert into lagou_job(title,url,url_object_id,job_desc,job_advantage,tags,
            crawl_time,company_name,company_url,job_addr,pulish_time,
            job_type,degree_need,work_years,job_city,salary_min) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON DUPLICATE KEY UPDATE salary_min=VALUES(salary_min),job_desc=VALUES(job_desc)
        '''

        params = (
            self['title'],self['url'],self['url_object_id'],self['job_desc'],self['job_advantage'],self['tags'],
            self['crawl_time'],self['company_name'],self['company_url'],self['job_addr'],self['pulish_time'],
            self['job_type'],self['degree_need'],self['work_years'],self['job_city'],self['salary_min'],
        )

        return insert_sql, params


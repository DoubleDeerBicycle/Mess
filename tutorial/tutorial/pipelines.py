# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import codecs,json
from scrapy.exporters import JsonItemExporter
import pymysql
from twisted.enterprise import adbapi
class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item

class JobbolePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok, value in results:
            image_file_path = value['path']
        item['post_image_path'] = image_file_path
        return item

#自定义json导出功能
class JsonPipeline(object):
    def __init__(self):
        self.file = codecs.open('jobbole.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False)+'\n'
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()

#调用scrapy提供的导出json接口
class JsonExporterPipeline(object):
    def __init__(self):
        self.file = open('json_jobbole.json','wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

#自定义mysql连接
class MysqlPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', user='root', password='1996', db='scrapy', port=3306)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = 'insert into jobbole(title,url,date,content,url_object_id) values (%s,%s,%s,%s,%s)'
        self.cursor.execute(insert_sql,(item['title'],item['url'],item['date'],item['content'],item['url_object_id']))
        self.conn.commit()


class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool
    
    @classmethod
    def from_settings(cls, settings):
        config = dict(
            host = settings['MYSQL_LOCALHOST'],
            db = settings['MYSQL_DB'],
            user = settings['MYSQL_USER'],
            password = settings['MYSQL_PASSWD'],
            cursorclass = pymysql.cursors.DictCursor,
            port = settings['MYSQL_PORT'],
            charset = 'utf8'
        )

        dbpool = adbapi.ConnectionPool('pymysql', **config)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handel_error)

    def handel_error(self, failure):
        print(failure)

    def do_insert(self, cursor, item):
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)
# -*- coding: utf-8 -*-
import base64
import hmac
import time
from hashlib import sha1
import re
import scrapy
import json
import datetime
from scrapy.loader import ItemLoader
from tutorial.items import ZhihuQuestionItem,ZhihuAnswerItem
from tutorial.settings import SQL_DATETIME_FORMAT,SQL_DATE_FORMAT
class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    #answer请求
    answer_url = 'https://www.zhihu.com/api/v4/questions/{id}/answers?include={include}&offset={offset}&limit={limit}&sort_by=default'
    answer_query = 'data[*].is_normal,admin_closed_comment,reward_info,is_collapsed,annotation_action,annotation_detail,collapse_reason,is_sticky,collapsed_by,suggest_edit,comment_count,can_comment,content,editable_content,voteup_count,reshipment_settings,comment_permission,created_time,updated_time,review_info,relevant_info,question,excerpt,relationship.is_authorized,is_author,voting,is_thanked,is_nothelp;data[*].mark_infos[*].url;data[*].author.follower_count,badge[*].topics'
    headers = {
        'Connection': 'keep-alive',
        'Referer': 'https://www.zhihu.com/signup?next=%2F',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    grant_type = 'password'
    client_id = "c3cef7c66a1843f8b3a9e6a1e3160e20"
    x_UDID = 'ANCuT28Zjg2PTn2VG48gf99U - sbL76I8EN4 ='
    source = 'com.zhihu.web'
    timestamp = str(int(time.time() * 1000))
    timestamp2 = str(time.time() * 1000)
    captcha_url = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=en'

    def parse(self, response):
        all_urls = response.css('a::attr(href)').extract()
        all_urls = [response.urljoin(url) for url in all_urls]
        all_urls = filter(lambda x: True if x.startswith('https') else False, all_urls)
        for url in all_urls:
            search_obj = re.search('(.*?question/(\d+))/.*?', url)
            if search_obj:
               request_url = search_obj.group(1)
               question_id = search_obj.group(2)
               yield scrapy.Request(response.urljoin(request_url), headers=self.headers, meta={'question_id':question_id},
                                    callback=self.parse_question)
            else:
                yield scrapy.Request(url, headers=self.headers, callback=self.parse)

    def parse_question(self, response):
        question_id = response.meta.get('question_id')
        content = re.search('.*?editableDetail":"(.*?)",',response.text, re.S).group(1)
        answer_num = int(re.search('.*?answerCount":(\d*),',response.text,re.S).group(1))
        comments_num = int(re.search('.*?commentCount":(\d*),', response.text, re.S).group(1))
        follower_user_num = int(re.search('.*?followerCount":(\d*),', response.text, re.S).group(1))
        visit_num = int(re.search('.*?visitCount":(\d*),', response.text, re.S).group(1))
        topics = response.css('#null-toggle::text').extract()
        if '默认排序' in topics:
            topics.remove('默认排序')
        topics = ','.join(topics)

        item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
        item_loader.add_css('title', 'h1.QuestionHeader-title::text')
        item_loader.add_value('url', response.url)
        item_loader.add_value('content', content)
        item_loader.add_value('zhihu_id', int(question_id))
        item_loader.add_value('answer_num', answer_num)
        item_loader.add_value('comments_num', comments_num)
        item_loader.add_value('follower_user_num', follower_user_num)
        item_loader.add_value('visit_num', visit_num)
        item_loader.add_value('topics', topics)
        item_loader.add_value('crawl_time', datetime.datetime.now().strftime(SQL_DATETIME_FORMAT))
        question_item = item_loader.load_item()
        yield scrapy.Request(self.answer_url.format(id=question_id, include=self.answer_query, offset=0, limit=20),
                             headers=self.headers, callback=self.parse_answer)
        yield question_item

    def parse_answer(self, response):
        ans_json = json.loads(response.text)
        is_end = ans_json['paging']['is_end']
        next_url = ans_json['paging']['next']

        #   提取answer的具体字段
        for answer in ans_json['data']:
            answer_item = ZhihuAnswerItem()
            answer_item['zhihu_id'] = answer['id']
            answer_item['url'] = answer['url']
            answer_item['question_id'] = answer['question']['id']
            answer_item['title'] = answer['question']['title']
            answer_item['headline'] = answer['author']['headline']
            answer_item['user_name'] = answer['author']['name']
            answer_item['author_id'] = answer['author']['id'] if 'id' in answer['author'] else None
            answer_item['content'] = answer['content'] if 'content' in answer else None
            answer_item['praise_num'] = answer['voteup_count']
            answer_item['comments_num'] = answer['comment_count']
            answer_item['create_time'] = datetime.datetime.fromtimestamp(answer['created_time']).strftime(SQL_DATETIME_FORMAT)
            answer_item['update_time'] = datetime.datetime.fromtimestamp(answer['updated_time']).strftime(SQL_DATETIME_FORMAT)
            answer_item['crawl_time'] = datetime.datetime.now().strftime(SQL_DATETIME_FORMAT)
            yield answer_item

        #   判断是否到达尾页
        if not is_end:
            yield scrapy.Request(next_url, headers=self.headers, callback=self.parse_answer)

    def start_requests(self):
        return [scrapy.Request(self.captcha_url, headers=self.headers, callback=self.login)]
    def login(self, response):
        need_cap = json.loads(response.body)['show_captcha']
        if need_cap:
            print("需要验证码")
            yield scrapy.Request(url=self.captcha_url, headers=self.headers,  callback=self.captcha, method='PUT')
        else:
            print("不需要验证码")
            post_url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
            post_data = {
                "client_id": self.client_id,
                "username": "1017592458@qq.com",
                "password": "z974624218",
                "source": self.source,
                "timestamp": self.timestamp,
                "signature": self.get_signature(self.grant_type, self.client_id, self.source, self.timestamp),
                "lang": "en",
                "ref_source": "homepage",
                "captcha": '',
            }
            yield scrapy.FormRequest(url=post_url, formdata=post_data, headers=self.headers, callback=self.check_login)

    def get_signature(self, grant_type, client_id, source, timestamp):
        """处理签名"""
        hm = hmac.new(b'd1b964811afb40118a12068ff74a12f4', None, sha1)
        hm.update(str.encode(grant_type))
        hm.update(str.encode(client_id))
        hm.update(str.encode(source))
        hm.update(str.encode(timestamp))
        return str(hm.hexdigest())

    def captcha(self, response):
        try:
            img = json.loads(response.text)['img_base64']
        except ValueError:
            print('获取img_base64失败')
        else:
            img = img.encode('utf8')
            img_data = base64.b64decode(img)

            with open('captcha.jpg', 'wb') as f:
                f.write(img_data)
                f.close()
        captcha = input('请输入验证码：')
        post_data = {'input_text': captcha}
        yield scrapy.FormRequest(url=self.captcha_url, formdata=post_data, callback=self.captcha_login, headers=self.headers)

    def captcha_login(self, response):
        try:
            cap_result = json.loads(response.body)['success']
        except ValueError:
            print('关于验证码的POST请求响应失败!')
        else:
            if cap_result:
                print('验证成功')
        post_url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
        post_data = {
            "client_id": self.client_id,
            "username": "1017592458@qq.com",
            "password": "z974624218",
            "grant_type": self.grant_type,
            "source": self.source,
            "timestamp": self.timestamp,
            "signature": self.get_signature(self.grant_type, self.client_id, self.source, self.timestamp),
            "lang": "en",
            "ref_source": "homepage",
            "captcha": '',
        }
        headers = self.headers
        headers.update({
            'Origin': 'https://www.zhihu.com',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'x-xsrftoken': 'UiFIIz9fMjuytEYZ7VViRIBKZugpWsEK',
            'X-Zse-83': '3_1.1',
            'x-requested-with': 'fetch',
        })
        yield scrapy.FormRequest(url=post_url, formdata=post_data, headers=headers, callback=self.check_login)

    def check_login(self, response):
        # 验证服务器的返回数据判断是否登录成功
        text_json = json.loads(response.text)
        if "uid" in text_json:
            for url in self.start_urls:
                yield scrapy.Request(url, dont_filter=True, headers=self.headers)

    # def start_requests(self):
    #     headers = {
    #         'cookie': '_zap=97a51395-2448-42ac-b04e-2f5bbc9450b2; d_c0="AOCvp8svjQ2PTmICE7m52zNxE_UrCEnJIZM=|1525593178"; _xsrf=QBZVH8jZRyAA2i7j5UWjAtk5jhRlGbvl; q_c1=30c044b4daf94a8a820ec4b2c5e7a329|1540096379000|1524299284000; tst=r; __utma=51854390.1380993689.1541054334.1541054334.1541054334.1; __utmz=51854390.1541054334.1.1.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/zhang-hao-hong-50/activities; __utmv=51854390.100-1|2=registration_date=20141030=1^3=entry_date=20141030=1; l_cap_id="NWU4Y2U4MGMzNzg2NGI4MTkwZjFjYzBhMTY0MjliMjU=|1541063326|76c6d3ee845c86c79f4aec2841ae04ea8097ab50"; r_cap_id="YTQ2MWEzNTgyYThiNDE3M2JjMWViYjMwM2I5MjgyNWI=|1541063326|d8cb3aa6074a67ed32223f3fb9460cd6e8f9a0c8"; cap_id="MjY4YjgxODY1NTEwNGYwYTgxYTU1ZDZiMzg3ZTRhNzY=|1541063326|ddd47fa771a10bf51d7de94532c1f3aeb7751d18"; __gads=ID=68e1cbdfb5f2c2c2:T=1541147832:S=ALNI_Mb_tVbCPrVyQ9l7i7yDw7DXEFw-DQ; capsion_ticket="2|1:0|10:1541232371|14:capsion_ticket|44:OTk4ZWFlNjcyZDdlNGZkNzhlYTQ0MjZjNTdmYWUyMzI=|93f8a30b1af5265c65c6f55a388f334a5e96d445d721a620c628b6be410eb004"; z_c0="2|1:0|10:1541232612|4:z_c0|92:Mi4xS18tWkFBQUFBQUFBNEstbnl5LU5EU1lBQUFCZ0FsVk41S1hLWEFCNVdsYjR4aGZnT0szMTFVdmpLX0lDaS10YXlB|b00bacb5d905e261ef3a9ce30fa1bcc9b2cdb20476638757b473fb44843d424a"; tgw_l7_route=4902c7c12bebebe28366186aba4ffcde',
    #         'Referer': 'https://www.zhihu.com/signin',
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    #     }
    #     yield scrapy.Request(url=self.start_urls[0], headers=headers)
    #     cookies = {
    #         '_zap': '97a51395-2448-42ac-b04e-2f5bbc9450b2',
    #         'd_c0': '"AOCvp8svjQ2PTmICE7m52zNxE_UrCEnJIZM=|1525593178"',
    #         '_xsrf': 'QBZVH8jZRyAA2i7j5UWjAtk5jhRlGbvl',
    #         'q_c1': '30c044b4daf94a8a820ec4b2c5e7a329|1540096379000|1524299284000',
    #         'tst': 'r',
    #         '__utma': '51854390.1380993689.1541054334.1541054334.1541054334.1',
    #         '__utmz': '51854390.1541054334.1.1.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/zhang-hao-hong-50/activities',
    #         '__utmv': '51854390.100-1|2=registration_date=20141030=1^3=entry_date=20141030=1',
    #         'l_cap_id': '"NWU4Y2U4MGMzNzg2NGI4MTkwZjFjYzBhMTY0MjliMjU=|1541063326|76c6d3ee845c86c79f4aec2841ae04ea8097ab50"',
    #         'r_cap_id': '"YTQ2MWEzNTgyYThiNDE3M2JjMWViYjMwM2I5MjgyNWI=|1541063326|d8cb3aa6074a67ed32223f3fb9460cd6e8f9a0c8"',
    #         'cap_id': '"MjY4YjgxODY1NTEwNGYwYTgxYTU1ZDZiMzg3ZTRhNzY=|1541063326|ddd47fa771a10bf51d7de94532c1f3aeb7751d18"',
    #         '__gads': 'ID=68e1cbdfb5f2c2c2:T=1541147832:S=ALNI_Mb_tVbCPrVyQ9l7i7yDw7DXEFw-DQ',
    #         'capsion_ticket': '"2|1:0|10:1541232371|14:capsion_ticket|44:OTk4ZWFlNjcyZDdlNGZkNzhlYTQ0MjZjNTdmYWUyMzI=|93f8a30b1af5265c65c6f55a388f334a5e96d445d721a620c628b6be410eb004"',
    #         'z_c0': '"2|1:0|10:1541232612|4:z_c0|92:Mi4xS18tWkFBQUFBQUFBNEstbnl5LU5EU1lBQUFCZ0FsVk41S1hLWEFCNVdsYjR4aGZnT0szMTFVdmpLX0lDaS10YXlB|b00bacb5d905e261ef3a9ce30fa1bcc9b2cdb20476638757b473fb44843d424a"',
    #         'tgw_l7_route': '931b604f0432b1e60014973b6cd4c7bc'
    #     }

    #     return[FormRequest('http://www.zhihu.com/', cookies=cookies, callback=self.parse)]

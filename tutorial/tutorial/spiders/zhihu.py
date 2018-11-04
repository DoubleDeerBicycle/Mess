# -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest
class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    def parse(self, response):
        print(response.text)


    def start_requests(self):
        headers = {
            'cookie': '_zap=97a51395-2448-42ac-b04e-2f5bbc9450b2; d_c0="AOCvp8svjQ2PTmICE7m52zNxE_UrCEnJIZM=|1525593178"; _xsrf=QBZVH8jZRyAA2i7j5UWjAtk5jhRlGbvl; q_c1=30c044b4daf94a8a820ec4b2c5e7a329|1540096379000|1524299284000; tst=r; __utma=51854390.1380993689.1541054334.1541054334.1541054334.1; __utmz=51854390.1541054334.1.1.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/zhang-hao-hong-50/activities; __utmv=51854390.100-1|2=registration_date=20141030=1^3=entry_date=20141030=1; l_cap_id="NWU4Y2U4MGMzNzg2NGI4MTkwZjFjYzBhMTY0MjliMjU=|1541063326|76c6d3ee845c86c79f4aec2841ae04ea8097ab50"; r_cap_id="YTQ2MWEzNTgyYThiNDE3M2JjMWViYjMwM2I5MjgyNWI=|1541063326|d8cb3aa6074a67ed32223f3fb9460cd6e8f9a0c8"; cap_id="MjY4YjgxODY1NTEwNGYwYTgxYTU1ZDZiMzg3ZTRhNzY=|1541063326|ddd47fa771a10bf51d7de94532c1f3aeb7751d18"; __gads=ID=68e1cbdfb5f2c2c2:T=1541147832:S=ALNI_Mb_tVbCPrVyQ9l7i7yDw7DXEFw-DQ; capsion_ticket="2|1:0|10:1541232371|14:capsion_ticket|44:OTk4ZWFlNjcyZDdlNGZkNzhlYTQ0MjZjNTdmYWUyMzI=|93f8a30b1af5265c65c6f55a388f334a5e96d445d721a620c628b6be410eb004"; z_c0="2|1:0|10:1541232612|4:z_c0|92:Mi4xS18tWkFBQUFBQUFBNEstbnl5LU5EU1lBQUFCZ0FsVk41S1hLWEFCNVdsYjR4aGZnT0szMTFVdmpLX0lDaS10YXlB|b00bacb5d905e261ef3a9ce30fa1bcc9b2cdb20476638757b473fb44843d424a"; tgw_l7_route=4902c7c12bebebe28366186aba4ffcde',
            'Referer': 'https://www.zhihu.com/signin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
        }
        yield scrapy.Request(url=self.start_urls[0], headers=headers)
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
        
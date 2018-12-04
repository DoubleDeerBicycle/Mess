# -*- coding: utf-8 -*-
import scrapy
import time


class TianyaSpider(scrapy.Spider):
    name = 'tianya'
    allowed_domains = ['tianya.cn']
    start_urls = ['http://bbs.tianya.cn/']

    # 定义请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3371.0 Safari/537.36'
    }

    def parse(self, response):
        pass

    # 请求登录url
    def start_requests(self):
        self.login_url = 'https://passport.tianya.cn/login'
        return [scrapy.Request(url=self.login_url, headers=self.headers, callback=self.login)]

    # 解析源码，获取表单中的参数
    def login(self, response):
        # 获取__sid
        sid = response.xpath('//input[@id="__sid"]/@value').extract_first()
        # 构造data
        data = {
            '__sid': sid,
            'vwriter': '我杯赛场',  # 用户名
            'action': 'f4.1543383689888.5045,b5.2.3|277f5a7b4c2c66405e4dd658ef76016b|359012274f74b93ba53ba5d830f7d6a9|Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3371.0 Safari/537.36|0|6|v2.2',
            'vpassword': '974624218',  # 密码
            'rmflag': '1'
        }
        # 判断是否需要输入验证码
        is_vc = response.xpath('//input[@name="vc"]').extract_first()
        if is_vc:
            # 请求验证码图片
            t = str(int(time.time()*1000))
            vc_url = 'https://imgcode.tianya.cn/services/ImageCodeService?_i={}'.format(t)
            # 定义验证码的请求头
            headers = {
                'Host': 'imgcode.tianya.cn',
                'Referer': 'https://passport.tianya.cn/login',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; `WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3371.0 Safari/537.36'
            }
            yield scrapy.Request(vc_url, headers=headers, meta={'data': data, 'is_vc': is_vc}, callback=self.login_vc)
        else:
            yield scrapy.Request(response.url, callback=self.login_vc, meta={'data': data, 'is_vc': is_vc}, dont_filter=True)

    # 验证码
    def login_vc(self, response):
        is_vc = response.meta.get('is_vc')
        data = response.meta.get('data')
        if is_vc:
            with open('vc.jpg', 'wb') as f:
                f.write(response.body)  # 将获取到的验证码写入本地
                f.close()
            data['vc'] = input('请输入验证码\n')
        return [scrapy.FormRequest(url=self.login_url, headers=self.headers, formdata=data, callback=self.check_login)]
    
    # 登录后
    def check_login(self, response):
        html = response.text
        pass



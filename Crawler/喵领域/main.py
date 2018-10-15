'''
目标网址：http://amlyu.com/
'''
import requests
import os
from requests.exceptions import RequestException
from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

class Amlyu:
    #预防反爬虫措施，返回请求头
    headers =  {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3371.0 Safari/537.36'
    }
    #请求首页，获取分类url
    def rq_index(self):
        try:
            resopnse = requests.get('http://amlyu.com/', headers=self.headers)
            if resopnse.status_code == 200:
                doc = pq(resopnse.text)
                category = doc('.sitenav ul li a').items()
                #用以存储分类URL
                self.category_url = []
                for url in category:
                    self.category_url.append(url.attr('href'))
                #因为后两个分类URL是开通会员以及注册，去掉它
                self.category_url.pop()
                self.category_url.pop(len(self.category_url)-1)
                print(self.category_url)
            else:
                return None
        except RequestException:
            return None
        
    #获取分类下当前页的所有图片url


amlyu = Amlyu()

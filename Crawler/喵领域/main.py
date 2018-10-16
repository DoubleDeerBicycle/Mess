'''
目标网址：http://amlyu.com/
注：如果控制台许久不更新，可能是服务器压力太大导致未响应，当出现这种情况请停止爬取
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
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from hashlib import md5
class Amlyu:
    #预防反爬虫措施，返回请求头
    def __init__(self):
        self.__headers =  {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3371.0 Safari/537.36'
        }
        #使用phantomjs爬取 禁止加载图片，提高爬取效率
        self.__dcap = dict(DesiredCapabilities.PHANTOMJS)
        #禁止加载图片
        self.__dcap["phantomjs.page.settings.loadImages"] = False 
        self.__browser = webdriver.PhantomJS(executable_path=r'D:\Program Files (x86)\phantomjs-2.1.1-windows\bin\phantomjs.exe' ,desired_capabilities=self.__dcap)
        
        #使用chrome爬取 禁止加载图片，提高爬取效率
        # self.__options = webdriver.ChromeOptions()
        # self.__prefs = {
        #     'profile.default_content_setting_values' : {
        #         'images' : 2
        #     }
        # }
        # self.__options.add_experimental_option('prefs',self.__prefs)        
        # self.__browser = webdriver.Chrome(chrome_options=self.__options)
        self.__wait = WebDriverWait(self.__browser,10)
    #请求首页，获取分类url
    def run(self):
        try:
            resopnse = requests.get('http://amlyu.com/', headers=self.__headers)
            if resopnse.status_code == 200:
                doc = pq(resopnse.text)
                category = doc('.sitenav ul li a').items()
                #用以存储分类URL
                self.__category_url = []
                for url in category:
                    self.__category_url.append(url.attr('href'))
                #因为后两个分类URL是开通会员以及注册，去掉它
                self.__category_url.pop()
                self.__category_url.pop(len(self.__category_url)-1)
                self.__get_category_url()
        except RequestException as e:
            print(e)
        
    #获取分类下当前页的图片集
    def __get_category_url(self):
        try:
            print('正在爬取图片集...')
            for url in self.__category_url:
                response = requests.get(url, headers=self.__headers)
                if response.status_code == 200:
                    self.__browser.get(url)
                    doc = pq(response.text)
                    images_url = []
                    self.__analytical_iamges(doc,images_url)
                    while doc.find('.container .pagination > ul .next-page > a'):
                        next_page = self.__wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.container .pagination > ul .next-page > a')))
                        next_page.click()
                        html = self.__browser.find_element_by_xpath("//*").get_attribute("outerHTML")
                        doc = pq(html)
                        self.__analytical_iamges(doc,images_url)                       
                    self.__get_image_url(images_url)
        except RequestException as e:
            print(e)
        except TimeoutException as e:
            print(e)
    
    #解析图片集中图片url的方法抽取
    def __analytical_iamges(self,doc,images_url):
        images = doc('.excerpts .excerpt > a').items()
        for url in images:
            images_url.append(url.attr('href'))

    #获取图片集中的图片url
    def __get_image_url(self,images_url):
        try:
            for url in images_url:
                response = requests.get(url,headers=self.__headers)
                if response.status_code == 200:
                    doc = pq(response.text)
                    images = doc('body > section > article > p img').items()
                    #图片集名称
                    self.__images_name = doc('body > div.focusbox > div > h1').text()
                    self.__image = []
                    for image in images:
                        self.__image.append(image.attr('src'))
                    self.__download_image()
        except RequestException as e:
            print(e)
    #下载图片
    def __download_image(self):
        #存放路径
        file_dir = os.getcwd()+'/file/图片/'+self.__images_name
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
            #写入
            print('下载 {}...'.format(self.__images_name) )
            for url in self.__image:
                content = requests.get(url).content
                with open(file_dir+'/'+md5(content).hexdigest()+'.jpg','wb') as f:
                    f.write(content)
        
#启动程序
amlyu = Amlyu()
amlyu.run()
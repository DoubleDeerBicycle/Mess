import re, os, requests, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.selector import Selector
from hashlib import md5
from requests.exceptions import RequestException
from urllib.parse import urljoin


class Budejie():
    def __init__(self):
        # 请求头
        self._headers = {
            'Cookie': '_ga=GA1.2.1463995867.1543021568; _gid=GA1.2.90421288.1543021568; Hm_lvt_7c9f93d0379a9a7eb9fb60319911385f=1543021568,1543021588,1543045666; Hm_lpvt_7c9f93d0379a9a7eb9fb60319911385f=1543045701',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3371.0 Safari/537.36'
        }
        # url
        self._index = 'http://www.budejie.com/'
        # 使用chrome爬取 禁止加载图片，提高爬取效率
        self.__options = webdriver.ChromeOptions()
        self.__prefs = {
            'profile.default_content_setting_values' : {
                'images' : 2
            }
        }
        self.__options.add_experimental_option('prefs',self.__prefs)        
        # 视频url
        self._video_url = 'http://www.budejie.com/video/'
        # 视频保存路径
        self._path = os.getcwd()+'/file/视频/百思不得姐/'
    # 链接请求
    def rq_index(self):
        try:
            # 引用chrome
            self._chrome = webdriver.Chrome(chrome_options=self.__options)
            # 超时等待调用
            self._wait = WebDriverWait(self._chrome, 10)
            # 判断是否点击下一页
            if self._chrome.current_url != 'data:,':
                self._index = self._chrome.current_url
            # 发出请求
            self._chrome.get(self._index)
            # 数据提取
            datas = self._data(self._chrome.page_source)
            for key, value in datas.items():
                # 调用数据保存模块
                self._down_image(key, value)

            # 判断是否存在下一页
            next_page = self._wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.pagenxt')))
            if next_page:
                next_page.click()
                self.rq_index()
            else:
                self._chrome.quit()
        except TimeoutError as e:
            print(e)

    # 数据提取
    def _data(self,html):
        # 使用selector解析
        doc = Selector(text=html)
        # 获取image地址与相关标题
        datas = doc.xpath('//a/img[@class="lazy"]').extract()
        # 用以存放解析后的数据键值对 标题-图片地址
        data_ok = {}
        # 解析数据
        for data in datas:
            try:
                name = re.search('.*?alt="(.*?)"', data).group(1)
                name = re.sub('\\u200b','',name)
                img_url = re.search('.*?data-original="(.*?)"', data).group(1)
                data_ok[name] = img_url
            except AttributeError as e:
                print(e)
        return data_ok

    # 图片数据保存
    def _down_image(self, name, img_url):
        name = re.sub('[ \/:*?"<>|".]', '', name)
        # 存放路径
        file_dir = os.getcwd()+'/file/图片/百思不得姐/'
        # 文件夹分类
        try:
            path = file_dir+name
            if not os.path.exists(path):
                os.makedirs(path)
            # 获取图片二进制并写入
            content = requests.get(img_url).content
            # md5生成图片名
            file_name = md5(content).hexdigest()
            with open(path+'/'+file_name+'.gif', 'wb') as f:
                print('{}开始下载..'.format(name))
                f.write(content)
        except FileNotFoundError as e:
            print(e)
    
    # 视频地址请求
    def rq_video(self, url):
        try:
            response = requests.get(url, headers=self._headers)
            if response.status_code == 200:
                doc = Selector(text=response.text)
                # 解析
                for data in self._video_data(doc):
                    # 下载数据
                    self._down_video(data.get('file_name'), data.get('url'))
                # 判断是否存在下一页
                next_page = doc.css('.pagenxt::attr(href)').extract_first()
                url = urljoin(self._video_url, next_page)
                self.rq_video(url)
            else:
                print('Access failed:{}'.format(response.status_code))
        except RequestException as e:
            print(e)

    # 视频数据解析    
    def _video_data(self, doc):
        videos = doc.css('.j-r-list-tool-l-down.f-tar').extract()
        for video in videos:
            try:
                yield{
                    'file_name': re.search('.*?data-text="(.*?)"', video, re.S).group(1),
                    'url': re.search('.*?href="(.*?mp4)"', video, re.S).group(1)
                }
            except AttributeError as e:
                print(e)
    # 视频数据保存
    def _down_video(self, file_name, url):
        path = self._path+file_name+'.mp4'
        content = requests.get(url).content
        with open(path, 'wb') as f:
            print('下载到:{}'.format(file_name))
            f.write(content)


bdj = Budejie()
# 图片下载
# bdj.rq_index()

# 视频下载
bdj.rq_video('http://www.budejie.com/video/')
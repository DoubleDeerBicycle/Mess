import requests
import re
import json
from scrapy.selector import Selector


class BaiDuDocument():
    def __init__(self, url):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
        }
        # 判断文档url是否正确
        if url != None and 'wenku.baidu.com/view' in url:
            self.url = url #文档URL
            self.type = None #文档类型（自动获取）
            self.title = None #文档名称（自动获取）
        else:
            self.url = None
            print('文档地址错误')
            exit()

    # 初始化参数值
    def getData(self):
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                response.encoding = 'gbk'
                self.type =  re.search(r"docType':.*?'(.*?)',", response.text).group(1)
                doc = Selector(text=response.text)
                title = doc.css('title::text').extract_first()
                self.title = re.search(r"title':.*?'(.*?)',", response.text).group(1)
        except Exception as e:
            print(e)
    def getDoc(self):
        pass
    

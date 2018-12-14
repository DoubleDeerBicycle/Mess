import requests
import re,os
from scrapy.selector import Selector
from urllib.parse import urljoin
import random
from hashlib import md5


class Maomi():
    def __init__(self):
        self.index = 'https://www.233ii.com/shipin/list-%E7%9F%AD%E8%A7%86%E9%A2%91.html'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3371.0 Safari/537.36',
            'cookie': '__cfduid=d812bdcf4314c876b7aa015bf1ec0d3431541315130',
            'upgrade-insecure-requests': '1',
            'if-range': '"5c0f2f45-19d27af"',
            'range': 'bytes=1267-1267'
        }

    def rq_index(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                response.encoding = 'utf-8'
                doc = Selector(text=response.text)
                next_url = doc.xpath('//a[contains(@title, "下一页")]/@href').extract_first()
                for datas in self.get_datas(doc):
                    self.down_video(datas.get('down_url'), datas.get('title'))
                if next_url:
                    self.rq_index(urljoin(self.index, next_url))
            else:
                print('HTTP error{}'.format(response.status_code))
        except Exception as e:
            print(url)
            print(e)
            
    def get_datas(self, doc):
        urls = doc.css('li.shown a::attr(href)').extract()
        for url in urls:
            url = urljoin(self.index, url)
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    response.encoding = 'utf-8'
                    doc = Selector(text=response.text)
                    down_url = doc.xpath('//input[@id="lin1k0"]/@value').extract_first()
                    title = doc.css('h2.c_pink.text-ellipsis::text').extract_first()
                    yield {
                        'down_url': down_url,
                        'title': title
                    }
                else:
                    print('HTTP error{}'.format(response.status_code))
            except Exception as e:
                print(url)
                print(e)

    def down_video(self, url, title):
        if url != None and title != None:
            file_name = re.sub('[ \/:*?"<>|\r".\n]', '', title)
            url = re.sub('one\.', '', url)
            dir_path = os.getcwd()+'/file/视频/猫咪/'
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            if file_name == '':
                file_name = chr(random.randint(1000, 2000))
            path = dir_path+file_name+'.mp4'
            if os.path.exists(path):
                print(file_name+'已存在，跳过下载')
            else:
                try:
                    response = requests.get(url, headers=self.headers)
                    if response.status_code == 200:
                        content = response.content
                        with open(path, 'wb') as f:
                            print('正在下载:'+file_name)
                            f.write(content)
                            f.close()
                    else:
                        print('HTTP error{}'.format(response.status_code))
                except Exception as e:
                    print(url)
                    print(e)
mao = Maomi()
mao.rq_index(mao.index)
# mao.rq_index('https://www.233ii.com/shipin/list-%E7%9F%AD%E8%A7%86%E9%A2%91-43.html')
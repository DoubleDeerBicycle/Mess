import requests
import os
import re
from scrapy.selector import Selector
from urllib.parse import urljoin
import time
import shutil


class Font():
    def __init__(self):
        self._url = 'http://font.knowsky.com/index_{}.htm'
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3371.0 Safari/537.36',
            'Referer': 'http://font.knowsky.com/',
            'Cookie': 'ASPSESSIONIDCQTQTCSC=DCGJDCCCFKFLIHBKAABAKFKN; Hm_lvt_d4e1f37236b971c11eed256014b19a11=1544256252,1544256265,1544256397,1544319337; UM_distinctid=16790c47e210-0a27d018de6918-7315394b-1fa400-16790c47e24900; CNZZDATA433095=cnzz_eid%3D1501793408-1544318908-%26ntime%3D1544318908; Hm_lpvt_d4e1f37236b971c11eed256014b19a11=1544322926'
        }
        response = requests.get(self._url.format('1'))
        response.encoding = 'utf-8'
        self._page = Selector(text=response.text).xpath('/html/body/div[2]/div[2]/div/div/div[1]/div[2]/div/div/a[6]/text()').extract_first()
        
    def _rq_index(self, num):
        try:
            response = requests.get(self._url.format(num))
            if response.status_code == 200:
                response.encoding = 'utf-8'
                doc = Selector(text=response.text)
                return doc
            else:
                return None
        except Exception as e:
            print(e)

    def _get_data(self):
        for num in range(1,int(self._page)+1):
            doc = self._rq_index(num)
            if doc:
                names = doc.css('.fontpic a::attr(title)').extract()
                urls = doc.css('.fontpic a::attr(href)').extract()
                images = doc.css('.fontpic a img::attr(src)').extract()
                for name,url,image in zip(names,urls,images):
                    yield{
                        'name': name,
                        'url': urljoin(self._url, url),
                        'image': image
                    }
            else:
                return None

    def down_data(self):
        # 根目录
        dir_path = os.getcwd()+'/file/字体/'
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        try:
            for datas in self._get_data():
                # 为所有字体创建单独的文件目录
                path = dir_path+datas.get('name')
                if not os.path.exists(path):
                    os.makedirs(path)
                    print('正在下载:'+datas.get('name'))
                    # 将字体图片写入到目录中
                    try:
                        response = requests.get(datas.get('image'))
                        if response.status_code == 200:
                            content = response.content
                            with open(path+'/'+datas.get('name')+'.jpg', 'wb') as f:
                                f.write(content)
                                f.close()
                    except Exception as e:
                        print(e)
                    # 获取字体下载地址
                    try:
                        response = requests.get(datas.get('url'))
                        if response.status_code == 200:
                            response.encoding = 'utf-8'
                            doc = Selector(text=response.text)
                            down_url = doc.xpath('//div[@class="xunlei"]/a[4]/@href').extract_first()
                            if down_url.rfind('.rar') == -1:
                                print(datas.get('name')+'需要付费下载，删除该文件夹..')
                                shutil.rmtree(path)
                            else:   
                                content = requests.get(down_url, headers=self._headers)
                                if content.status_code == 200:
                                    with open(path+'/'+datas.get('name')+'.rar', 'wb') as f:
                                        f.write(content.content)
                                        f.close()
                                else:
                                    print(content.status_code)
                    except Exception as e:
                        print(e)
                    # 降低爬虫爬取速度
                    time.sleep(1)
                else:
                    print(datas.get('name')+'已存在，跳过下载')
        except Exception as e:
            print(e)
        

font = Font()
font.down_data()
#有几天没写爬虫了，现在练练手
#目标网址：https://yaoshe26.com/categories/ 该url下存在多个类别，需要将所有分类下的url获取

from pyquery import PyQuery as pq
import requests,re,math,os
from requests.exceptions import RequestException
from urllib.parse import urlencode

class Yaoshe():
    def __init__(self):
        #如果服务器无响应，加上请求头
        self._headers = {
            'referer': 'https://yaoshe26.com/',
            'cookie': '__cfduid=d4674843ded61ce74d647c3decc7f5cbe1541229514; _ga=GA1.2.649845522.1541229517; _gid=GA1.2.102003991.1541229517; UM_distinctid=166d8701d3c3fe-04a74968579a4d-7315394b-1fa400-166d8701d3e3ce; kt_tcookie=1; kt_is_visited=1; PHPSESSID=vpqp4j817angp76f4oaeku2gf2; CNZZDATA1264603175=972749599-1541229491-%7C1541294318',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3371.0 Safari/537.36'
        }
        html = None
        try:
            response = requests.get('https://yaoshe26.com/categories/', headers=self._headers)
            if response.status_code == 200:
                html = response.text
        except RequestException as e:
            print(e)

        self._doc = None
        if html:
            self._doc = pq(html)

    

    #获取所有分类url
    def get_categories_url(self):
        if self._doc:
            categories_urls = self._doc('#list_categories_categories_list_items a').items()
            self._categories = {}
            for cg_url in categories_urls:
                self._categories[cg_url.attr('href')] = cg_url.attr('title')+cg_url.find('.wrap .videos').text()


    #遍历分类，并获取该分类下所有url
    def get_movie_url(self):
        index = 0
        for url in self._categories.keys():
            try:
                nums = int(re.search('.*?(\d+)', self._categories.get(url)).group(1))
                page_end = math.ceil(nums/30)
                for num in range(1,page_end+1):
                    data = {
                        'mode': 'async',
                        'function': 'get_block',
                        'block_id': 'list_videos_common_videos_list',
                        'sort_by': 'video_viewed',
                        'from': num
                    }
                    data_url = url+'?'+urlencode(data)
                    response = requests.get(data_url, headers=self._headers)
                    if response.status_code == 200:
                        doc = pq(response.text)
                        cg_name = self._categories.get(url)
                        for datas in self._next_page(doc, cg_name):
                            self._download(datas)
                index += 1
            except RequestException as e:
                print(e)


    #翻页方法的抽取
    def _next_page(self, doc, cg_name):
        urls = doc('#list_videos_common_videos_list_items .item a').items()
        for url in urls:
            yield {
                'cg_name': cg_name,
                'url': url.attr('href'),
                'title': url.find('.img img').attr('alt'),
                'date': url.find('.wrap .duration').text()
            }


    #保存到本地
    def _download(self, datas):
        file_dir = os.getcwd()+'/file/其他/'
        name = datas.get('cg_name')
        with open(file_dir+name+'.txt','a',encoding='utf-8') as f:
            print('正在写入:'+datas.get('title'))
            f.write('片名:'+datas.get('title')+'\t时长:'+datas.get('date')+'\t地址:'+datas.get('url')+'\n')

yaoshe = Yaoshe()
yaoshe.get_categories_url()
yaoshe.get_movie_url()

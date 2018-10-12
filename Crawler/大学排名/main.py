"""
网址：http://www.zuihaodaxue.com/
分析：主要爬取中国大学排名以及世界大学排名这两个栏目
"""
import requests
from requests.exceptions import RequestException
from pyquery import PyQuery as pq

index_url = 'http://www.zuihaodaxue.com/'
#获得中国大学以及世界大学排名的栏目url
def get_column_url(index_url):
    try:
        response = requests.get(index_url)
        if response.status_code == 200:
            doc = pq(response.text)
            #中国大学url
            china_university = doc('#top-menu > li:nth-child(2) > a').attr('href')
            #世界大学url
            world_university = doc('#top-menu > li:nth-child(3) > a').attr('href')
            
            if china_university and world_university:
                return {
                'china':index_url+china_university,
                'world':index_url+world_university
                }
            else:
                return None
        return None
    except RequestException:
        return None

#获取栏目下所有的排名url
def get_all_url(dict_url):
    global index_url
    chian_url = []
    world_url = []
    if dict_url:
        try:
            #中国大学栏目url
            cn = requests.get(dict_url.get('china'))
            if cn.status_code == 200:
                doc = pq(cn.text)
                #获取中国大学栏目下的所有url
                cn_urls = doc('.smallpic a').items()
                for url in cn_urls:
                    chian_url.append(index_url+url.attr('href'))
            
            #世界大学栏目url
            wd = requests.get(dict_url.get('world'))
            if wd.status_code == 200:
                doc = pq(wd.text)
                wd_urls = doc('.bigpic a').items()
                for url in wd_urls:
                    if not world_url.count(index_url+url.attr('href')):
                        world_url.append(index_url+url.attr('href'))
            
            return {
                'cn_urls':chian_url,
                'wd_urls':world_url
            }
        except RequestException:
            return None

#分析网页结构并抓取数据
def get_data(dict_list_url):
    cn_urls = dict_list_url.get('cn_urls')
    if cn_urls:
        for url in cn_urls:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    response.encoding = 'utf-8'
                    doc = pq(response.text)
                    td = doc('.alt').items()
                    for i in td:
                        print(i)
            except RequestException:
                return None
def main():
    global index_url
    dict_list_url = get_all_url(get_column_url(index_url))
    get_data(dict_list_url)
main()
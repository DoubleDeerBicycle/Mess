"""
网址：http://www.zuihaodaxue.com/
主要爬取中国大学排名
"""
import requests
from requests.exceptions import RequestException
from pyquery import PyQuery as pq
import os
index_url = 'http://www.zuihaodaxue.com/'
#获得中国大学以及世界大学排名的栏目url
def get_column_url(index_url):
    try:
        response = requests.get(index_url)
        if response.status_code == 200:
            doc = pq(response.text)
            #中国大学url
            china_university = doc('#top-menu > li:nth-child(2) > a').attr('href')          
            if china_university:
                return {
                'china':index_url+china_university,
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
                     
            return {
                'cn_urls':chian_url,
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
                    td_list = doc('.alt').items()
                    for td in td_list:
                        yield {
                            't1':td.find('td:nth-child(1)').text(),
                            't2':td.find('td:nth-child(2) > div').text(),
                            't3':td.find('td:nth-child(3)').text(),                     
                            't4':td.find('td:nth-child(4)').text(),
                            't5':td.find('td:nth-child(5)').text()  
                        }       
            except RequestException:
                return None
#获取表格头信息以及网页名并写入                
def get_title(dict_list_url):
    cn_urls = dict_list_url.get('cn_urls')
    #如果目录不存在则创建
    file_dir = os.getcwd()+'/file/'
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    if cn_urls:
        for url in cn_urls:
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    response.encoding = 'utf-8'
                    doc = pq(response.text)
                    #网页名
                    title = doc('body > div.container > div > div.col-lg-9.col-md-9.col-sm-9.col-xs-12 > div > h3').text()
                    #表格头部信息
                    print(title)
                    f_write = open(file_dir+title+'.txt','a',encoding='utf8')
                    f_write.write(doc('body > div.container > div > div.col-lg-9.col-md-9.col-sm-9.col-xs-12 > div > div.news-blk > div > table > thead > tr > th:nth-child(1)').text()+'\t')
                    f_write.write(doc('body > div.container > div > div.col-lg-9.col-md-9.col-sm-9.col-xs-12 > div > div.news-blk > div > table > thead > tr > th:nth-child(2)').text()+'\t')
                    f_write.write(doc('body > div.container > div > div.col-lg-9.col-md-9.col-sm-9.col-xs-12 > div > div.news-blk > div > table > thead > tr > th.hidden-xs').text()+'\t')
                    f_write.write(doc('body > div.container > div > div.col-lg-9.col-md-9.col-sm-9.col-xs-12 > div > div.news-blk > div > table > thead > tr > th:nth-child(4)').text()+'\t')
                    f_write.write(doc('body > div.container > div > div.col-lg-9.col-md-9.col-sm-9.col-xs-12 > div > div.news-blk > div > table > thead > tr > th:nth-child(5)').text()+'\n')                    
                    datas = get_data(dict_list_url)
                    for data in datas:
                        download(data,f_write)
                        print('-'*50)
            except RequestException:
                return None
#写入数据到本地
def download(data,f_write):
    # f_write.write(data.get('t1')+'\t\t')
    # f_write.write(data.get('t2')+'\t')
    # f_write.write(data.get('t3')+'\t')
    # f_write.write(data.get('t4')+'\t\t\t')
    # f_write.write(data.get('t5')+'\n')
    print(data.get('t1'))
    print(data.get('t2'))
    print(data.get('t3'))
    print(data.get('t4'))
    print(data.get('t5'))
def main():
    global index_url
    #获取所有url
    dict_list_url = get_all_url(get_column_url(index_url))
    #创建文件以及写入表格头
    get_title(dict_list_url)
    
main()
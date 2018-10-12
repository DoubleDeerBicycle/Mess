from urllib.parse import urlencode
from requests.exceptions import ConnectionError
import requests
from pyquery import PyQuery as pq
import re
import pymongo

client = pymongo.MongoClient('localhost')
db = client['weixin']
base_url = 'http://weixin.sogou.com/weixin?'

headers = {
    'Cookie': 'CXID=EC189A21FE23D0A84130DE581166C9C5; SUID=1FE39F273665860A5AE97A08000C4461; IPLOC=CN3601; SUV=005607F527A71BFC5B122864DCDBF467; usid=FC1BA727AD3E990A000000005B12286B; SMYUV=1532323955127191; UM_distinctid=164c5a002f920f-0259b7ffb05526-7315394b-1fa400-164c5a002fa27; wuid=AAF1nTcHIgAAAAqLK0axuw4AGwY=; sw_uuid=6568729744; sg_uuid=6234029808; dt_ssuid=5836340572; pex=C864C03270DED3DD8A06887A372DA219231FFAC25A9D64AE09E82AED12E416AC; ssuid=1877273032; pgv_pvi=5640400896; ad=ukllllllll2zfgowlllllVm1qQGlllllJi@04Zllll9llllllZlll5@@@@@@@@@@; ABTEST=7|1538978052|v1; weixinIndexVisited=1; SUIR=34FCD742666311D7257EED3266274FFE; SNUID=D51F36A28481F346EFE07CA985CA51BC; ppinf=5|1539061018|1540270618|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZToyNzolRTclQUIlQTAlRTYlQjUlQTklRTYlQjQlQUF8Y3J0OjEwOjE1MzkwNjEwMTh8cmVmbmljazoyNzolRTclQUIlQTAlRTYlQjUlQTklRTYlQjQlQUF8dXNlcmlkOjQ0Om85dDJsdUlQYnRJUkVTSS1DUm9iMzQxWlJGbWNAd2VpeGluLnNvaHUuY29tfA; pprdig=Xpzu1SDnDM8PxuN-l4uifYhQuvqD0GXbrg9gLWOw8rojq1Qdbq018Rf_MdKOEMjU_2g70QWpuc_tyoVFHz6vu3x9bXahMFtmdvwMermxzlkeuV0eBozJklL2ddFMFTHn7FT3iOOPXZKjEQV-DHa5wcXzNtbAfEGi2M9oXrXXGKI; sgid=16-37422707-AVu8NRrN0NNrAFiaiaiawCVbibU; ppmdig=1539136720000000668c28420df92ddf57c3732658fce99a; sct=17; JSESSIONID=aaaASofRSemt5dDlliszw',
    'Host': 'weixin.sogou.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3371.0 Safari/537.36'
}
proxy_pool_url = 'http://127.0.0.1:5555/get'
proxy = None
def get_proxy():
    try:
        response = requests.get(proxy_pool_url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None
def get_html(url):
    global proxy
    try:
        if proxy:
            proxies = {
                'http': 'http://'+proxy
            }
            response = requests.get(url, allow_redirects=False, headers=headers, proxies=proxies)
        else:
            response = requests.get(url, allow_redirects=False, headers=headers)
        if response.status_code == 200:
            return response.text
        if response.status_code == 302:
            print('302')
            
            proxy = get_proxy()
            if proxy:
                print('Using proxy', proxy)
                return get_html(url)
            else:
                print('Get Proxy Failed')
                return None
    except ConnectionError as e:
        print('error', e.args)
        proxy = get_proxy()
        return get_html(url)

def get_index(keyword,page):
    data = {
        'query': keyword,
        'type': '2',
        'page': page,
    }
    url = base_url+urlencode(data)
    html = get_html(url)
    return html

def pares_index(html):
    doc = pq(html)
    items = doc('.wrapper .main-left .news-box .news-list li .txt-box h3 a').items()
    for item in items:
        yield item.attr('href')

def get_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None

def parse_detail(html):
    # print(html)
    doc = pq(html)
    title = doc('.rich_media_title').text()
    content = doc('.rich_media_content ').text()
    date = re.search(r'.*?publish_time = "(.*?)"',html,re.S)
    if not date:
        date = ''
    else:
        date = date.group(1)
    nickname = doc('#js_name').text()
    wechat = doc('#js_profile_qrcode > div > p:nth-child(3) > span').text()
    return {
        'title':title,
        'content':content,
        'date':date,
        'nickname':nickname,
        'wechat':wechat
    }
    
def save_to_mongo(data):
    if db['articles'].update({'title':data['title']},{'$set':data},True):
        print('Saved to Mongo',data['title'])
    else:
        print('Saved to Mongo Failed',data['title'])
def main():
    for page in range(1, 101):
        html = get_index('风景', page)
        if html:
            article_urls = pares_index(html)
            for article_url in article_urls:
                article_html = get_detail(article_url)
                save_to_mongo(parse_detail(article_html))
if __name__ == '__main__':
    main()
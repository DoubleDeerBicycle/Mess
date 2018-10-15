import requests
import re
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
from hashlib import md5
import os

err_num = 0
text_class = '自拍偷拍'
def get_header():
    return {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3371.0 Safari/537.36'
    }
def get_html(url):
    html_text = requests.get(url,headers = get_header())
    try:
        if html_text.status_code == 200:
            html_text.encoding = 'utf-8'
            return html_text.text
    except RequestException:
        print ('访问类别链接失败')
        return None

def page_class():
    print ('1.自拍偷拍  2.亚洲色图  3.欧美色图  4.美腿丝袜  5.清纯唯美  6.乱伦熟女  7.卡通动漫')
    page_directory = input('请输入对应的序号:')
    page_text = input('需要爬取多少页?')

    global text_class
    page = 1
    try:
        page = int(page_text)
        if page_directory == '1':
            pass
        elif page_directory == '2':
            text_class = '亚洲色图'
        elif page_directory == '3':
            text_class = '欧美色图'
        elif page_directory == '4':
            text_class = '美腿丝袜'
        elif page_directory == '5':
            text_class = '清纯唯美'
        elif page_directory == '6':
            text_class = '乱伦熟女'
        elif page_directory == '7':
            text_class = '卡通动漫'
        else:
            print ('请输入1-8之间的序号')
    except ValueError:
        print ('页数中包含非数字字符')
        return
    for i in range(1,page+1):
        yield{
            'url':'https://www.908ii.com/tupian/list-'+text_class+'-'+str(i)+'.html',
            'text_class':text_class
        }
def get_image_css(url):
    html_text = get_html(url)
    if html_text != None:
        soup = BeautifulSoup(html_text,'lxml')
        css_id = soup.select('#tpl-img-content')
        
        image_url = re.findall('href="(.*?)"',str(css_id),re.S)
        top = 'https://www.908ii.com'
        for image in image_url:
            yield top + image

def open_image_url(url):
    response = requests.get(url,headers = get_header())
    try:
        if response.status_code == 200:
            response.encoding = 'utf-8'
            yield response.text
        return None
    except RecursionError:
        print ('打开图片链接失败')
        global err_num
        err_num+=1
        if err_num >= 3:
            print ('爬取结束')
            exit()
def get_image_url(url):
    image_html = url
    if image_html != None:
        soup = BeautifulSoup(image_html,'lxml')
        title = str(soup.title.string).strip()
        
        content = soup.select('.content')
        image_url = re.findall('data-original="(.*?)"',str(content),re.S)
        yield{
            'title':title,
            'image_url':image_url
        }

def image_content(url):
    print ('正在下载:',url)
    respone = requests.get(url,headers = get_header())
    try:
        if respone.status_code == 200:
            yield respone.content
        return None
    except RequestException:
        print ('解析图片失败')
        return None
def download_image(url,title):
    global text_class
    if not os.path.exists(os.getcwd()+'/file/图片/{}-{}'.format(text_class,title)):
        os.makedirs(os.getcwd()+'/file/图片/{}-{}'.format(text_class,title))
    for image_url in url:
        for content in image_content(image_url):
            file_path = os.getcwd()+'/file/图片/{}-{}/{}.png'.format(text_class,title,md5(content).hexdigest())
            if not os.path.exists(file_path):
                with open(file_path,'wb') as f:
                    f.write(content)
                    f.close()
        
def main():
    for i in page_class():
        for url in get_image_css(i.get('url')):
            for image_text in open_image_url(url):
                # print (image_text)
                for image_url in get_image_url(image_text):
                    # print (image_url.get('title'))
                    # print (image_url.get('image_url'))
                    download_image(image_url.get('image_url'),image_url.get('title'))
            

if __name__ == '__main__':
    main()
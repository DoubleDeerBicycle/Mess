import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import re
import os

err_num = 0
def set_header():
    return {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3371.0 Safari/537.36'
    }
def get_html(url):
    try:
        html = requests.get(url,headers = set_header())
        if html.status_code == 200:
            html.encoding = 'utf-8'
            return html.text
        return None
    except RequestException:
        print ('访问类目链接失败')
        return None



def page_class():
    print ('1.都市激情  2.人妻交换  3.校园春色  4.家庭乱伦  5.情色笑话  6.性爱技巧  7.武侠古典  8.另类小说')
    text_directory = input('请输入对应的序号')
    text_page = input('需要爬取多少页？')
    text_class = '都市激情'

    page = 1
    try:
        directory = int(text_directory)
        page = int(text_page)
        if directory == 1:
            text_class = '都市激情'
        elif directory == 2:
            text_class = '人妻交换'
        elif directory == 3:
            text_class = '校园春色'
        elif directory == 4:
            text_class = '家庭乱伦'
        elif directory == 5:
            text_class = '情色笑话'
        elif directory == 6:
            text_class = '性爱技巧'
        elif directory == 7:
            text_class = '武侠古典'
        elif directory == 8:
            text_class = '另类小说'
        else:
            print ('请输入1-8之间的序号')
    except ValueError:
        print ('序号中包含未知数字')
        return
    for i in range(1,page+1):
        # yield 'https://www.908ii.com/xiaoshuo/list-'+text_class+'-'+str(i)+'.html'
        yield {
            'url':'https://www.908ii.com/xiaoshuo/list-'+text_class+'-'+str(i)+'.html',
            'cla':text_class
        }

def get_text_url(html):
    if html !=None:
        soup = BeautifulSoup(html,'lxml')
        css_class = soup.select('.text-list-html ul')
        
        text_css = str(css_class)

        top = 'https://www.908ii.com'

        text_html = re.findall('href="(.*?)"',text_css,re.S)
        
        for i in text_html:
            yield top+i
            # print (top+i)

def get_text(url): 
    try:
        response = requests.get(url,headers = set_header())
        if response.status_code == 200:
            response.encoding = 'utf-8'
            yield response.text
        return None
    except RequestException:
        print ('打开小说链接失败')
        global err_num
        err_num += 1
        if err_num >= 3:
            print ('爬取结束')
            exit()

def download_text(get_text_url,cla):
    for texts in get_text(get_text_url):
        if texts != None:
            soup = BeautifulSoup(texts,'lxml')
            title = soup.title.string
            title = str(title).strip()
            # print (title)
            text = soup.select('.content')
            text = str(text)
            # print (text)
            analytical_text = re.search('<br/>\n(.*?)</div>',text,re.S)
            place_text = re.sub(r'<br/>|<p>|</p>','\n',analytical_text.group(1))
            if not os.path.exists(os.getcwd()+'/file/小说'):
                os.makedirs(os.getcwd()+'/file/小说')
            file_path = os.getcwd()+'/file/小说/{}-{}.txt'.format(cla,title)
            if not os.path.exists(file_path):
                with open(file_path,'w',encoding='utf-8') as f:
                    f.write(place_text)
                    print ('正在下载:',title)
                    f.close
def main():
    for html in page_class():
        html_text = get_html(html.get('url'))
        for text_url in get_text_url(html_text):
            download_text(text_url,html.get('cla'))


if __name__ == '__main__':
    main()

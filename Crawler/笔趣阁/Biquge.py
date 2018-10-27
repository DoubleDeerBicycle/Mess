import re
from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException
import os
#小说名
bookName = None

def header():
    return {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3371.0 Safari/537.36'
    }

#请求链接
def get_txt_url(url):
    try:
        response = requests.get(url,headers = header())
        if response.status_code == 200:
            response.encoding = 'GBK'
            return response.text
        return None
    except RequestException:
        print ('请求链接失败')
        exit()

#获取目录下的所有目录链接,并解析
def bs_get_url(html):
    soup = BeautifulSoup(html,'lxml')
    str_soup = str(soup)

    global bookName
    #获取小说名
    re_bookName = re.search('.*?<h1>(.*?)</h1>',str_soup,re.S)
    bookName = re_bookName.group(1)
    # 获取章节
    chapterList = soup.select('#list dl dd')

    chapterName = re.findall('.*?href="(.*?)">',str(chapterList),re.S)

    index_url = 'http://www.biquge.com.tw'
    for name in chapterName:
        try:
            url_chapter = requests.get(index_url+name,headers = header())
            if url_chapter.status_code == 200:
                url_chapter.encoding = 'GBK'
                yield url_chapter.text

        except RequestException:
            print ('解析章节失败')
            return None
#提取章节名与内容
def split_chapter(html):
    soup = BeautifulSoup(html,'lxml')
    title = soup.select('.bookname h1')
    chapter_name = re.search('.*?<h1>(.*?)</h1>',str(title))

    text_main = soup.select('#content')

    title_name = chapter_name.group(1)

    text = re.search('.*?content">(.*?)</div>',str(text_main),re.S)

    text_event = re.sub(r'<br/>','',text.group(1))
    yield{
        'name':title_name,
        'text':text_event
    }
#下载章节保存到本地
def download_text(yl_url):
    global bookName
    file_dir = os.getcwd()+'/file/小说/'
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    with open(file_dir+bookName+'.txt','a',encoding='utf-8') as f:
        print ('已下载到:'+yl_url.get('name'))
        f.write(yl_url.get('name')+'\n'+yl_url.get('text')+'\n')
def main():
    url = input('请输入笔趣阁小说链接\n')
    if 'http://www.biquge.com.tw' in url:
        for chapter_url in bs_get_url(get_txt_url(url)):
            for text in split_chapter(chapter_url):
                download_text(text)
        print ('下载完成')
    else:
        print ('请输入笔趣阁链接')
        exit()
if __name__ == '__main__':
    main()
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pyquery import PyQuery as pq
import os
browser = webdriver.Chrome()
wait = WebDriverWait(browser,10)
#用以判断小说是否正常下载完成,0为正常，1为异常
changes = 0
#网站首页
index_html = 'http://www.biquge.com.tw/'
#书名
BOOKNAME = None
def start_browser():
    try:
        global index_html
        browser.get(index_html)
        #搜索
        input_bookname = input('输入书名(无法保证是否全本)\n')
        elemt = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#wd')))
        elemt.send_keys(input_bookname)
        sublit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#sss')))
        sublit.click()

        #切换到搜索后跳转的页面
        window = browser.current_window_handle
        windows = browser.window_handles
        for current_window in windows:
            if current_window != window:
                browser.switch_to_window(current_window)
        #返回搜索结果进行页面判断
        html = browser.page_source
        return html
    except TimeoutException:
        global changes
        print ('连接超时,请重试')
        changes = 1
def get_nr(nr,book_list):
    for i in nr:
        url = i.find('.odd > a').attr('href')
        name = i.find('.odd > a').text()
        book_list[name] = url
def get_html(doc):
    global index_html
    global  BOOKNAME
    #获取书名
    BOOKNAME = doc.find('#info > h1').text()
    # 获取所有的章节数
    a_url_num = doc.find('#list > dl > dd > a').items()
    # 获取到第一章链接
    a_url_one = doc.find('#list > dl > dd > a').attr('href')
    return {
        'url': index_html + a_url_one,
        'url_num': a_url_num
    }
def get_html_judge(html):
    doc = pq(html)
    if doc.find('#list'):
         return get_html(doc)
    elif doc.find('#nr'):
        #该页面有多个选择
        print ('已进入模糊查询,正在查找所有符合查找条件的小说...')
        #获取当前页面的源码
        html = browser.page_source
        doc = pq(html)
        #用于存储小说名以及小说链接
        book_list = {}
        nr = doc.find('#nr').items()
        get_nr(nr,book_list)
        #存在下一页
        while doc.find('#pagelink > a.next'):
            next_page = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#pagelink > a.next')))
            next_page.click()
            html = browser.page_source
            doc = pq(html)
            nr = doc.find('#nr').items()
            get_nr(nr,book_list)
        for book_name in book_list.keys():
            print (book_name)
        input_book_name = input('请输入你要下载的书名\n')
        if book_list.get(input_book_name):
            browser.get(book_list.get(input_book_name))
            html = browser.page_source
            doc = pq(html)
            return get_html(doc)
        else:
            while not book_list.get(input_book_name):
                input_book_name = input('请输入屏幕中存在的书名(如果需要退出请输入quit)\n')
                if input_book_name == 'quit':
                    global changes
                    changes = 2
                    return
            browser.get(book_list.get(input_book_name))
            html = browser.page_source
            doc = pq(html)
            return get_html(doc)
    else:
        #未找到小说
        print ('未找到该小说')
        changes = 1
#解析章节内容
def get_url_text(a_url_dict):
    try:
        browser.get(a_url_dict.get('url'))
        num = a_url_dict.get('url_num')
        for a in num:
            next_page = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="wrapper"]/div[4]/div/div[4]/a[4]')))
            #获取当前章节的内容，以及章节名称
            html = browser.page_source
            doc = pq(html)
            #章节名称
            chapterName = doc.find('#wrapper > div.content_read > div > div.bookname > h1').text()
            #章节内容
            chapterText = doc.find('#content').text()
            yield {
                'name':chapterName,
                'text':chapterText
            }
            next_page.click()
    except TimeoutException:
        get_url_text(a_url_dict)

#开始下载
def download_text(name,text):
    global BOOKNAME
    file_dir = os.getcwd()+'/file/小说/'
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)
    with open(file_dir+BOOKNAME+'.txt','a',encoding='utf-8') as f:
        print ('下载到:'+name)
        f.write(name+'\n'+text+'\n')
        
def main():
    try:
        chapterList = get_html_judge(start_browser())
        if chapterList:
            for list in get_url_text(chapterList):
                download_text(list.get('name'), list.get('text'))
    finally:
        browser.close()
        browser.quit()
        global changes
        if changes == 1:
            print ('下载失败')
        elif changes == 2:
            pass
        else:
            print ('下载成功')
if __name__ == '__main__':
    main()

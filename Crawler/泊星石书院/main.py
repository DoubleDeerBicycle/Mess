from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import re
from time import sleep
import os
browser = webdriver.Chrome()
wait = WebDriverWait(browser,10)
browser.maximize_window()
changs = 0
def get_doc():
    try:
        browser.get('https://www.mkxs8.com/')
        input_ = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="searcharticle"]/div/input[1]')))

        input_bookname = input('请输入书名\n')
        input_.send_keys(input_bookname)

        sublit = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="button"]')))
        sublit.click()

        html = browser.find_element_by_xpath("//*").get_attribute("outerHTML")
        return html
    except TimeoutException:
        print ('连接超时')
        global changs
        changs = 1

def is_items(html):
    doc = pq(html)
    if doc.find('#content'):
        get_read_url = doc.find('#content > div.Sum > ul > li.button2.white > a:nth-child(1)').attr('href')
        return get_read_url
    elif doc.find('#content2 .odd'):
        booklist = {}
        print ('已进入模糊搜索，正在查询所有符合条件的数据...')
        get_book_url(booklist,doc)
        while doc.find('#pagelink > a.next'):
            page_next = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#pagelink > a.next')))
            sleep(1)
            page_next.click()
            html = browser.find_element_by_xpath("//*").get_attribute("outerHTML")
            doc = pq(html)
            get_book_url(booklist,doc)
        for name in booklist.keys():
            print (name)
        find_name = input('输入屏幕中出现的书名\n')
        if booklist.get(find_name):
            browser.get(booklist.get(find_name))
            html = browser.find_element_by_xpath("//*").get_attribute("outerHTML")
            doc = pq(html)
            return doc.find('#content > div.Sum > ul > li.button2.white > a:nth-child(1)').attr('href')
        else:
            global changs
            changs = 1
    else:
        print ('未找到该小说')
        changs = 1
def get_book_url(booklist,doc):
    url_name = doc.find('.odd')
    str_url_name = str(url_name)
    urllist = re.findall('.*?href="(.*?)"', str_url_name, re.S)
    namelist = re.findall('.*?href.*?">(.*?)</a>', str_url_name, re.S)
    for i in range(len(urllist)):
        booklist[namelist[i]] = urllist[i]
def get_chapter(url):
        browser.get(url)
        html = browser.page_source
        bookname = re.search('.*?<h1>(.*?)</h1>', html, re.S)
        file_dir = os.getcwd() + '/file/小说/'
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        f_write = open(file_dir + bookname.group(1) + '.txt', 'a')
        start_a = re.search('box-item.*?rel.*?href="(.*?)">.*?</a>', html, re.S)
        browser.get(url + start_a.group(1))
        next_page = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#nextLink')))
        while next_page:
            try:
                title = re.search('.*?chapter_title"><h1>(.*?)</h1', browser.page_source, re.S)
                text = re.search('.*?text_area">(.*?)</div>', browser.page_source, re.S)
                print('下载到:' + title.group(1))
                text = re.sub(r'<br />','\n',text.group(1))
                f_write.write(title.group(1) + '\n' + text + '\n')
                next_page.click()
                next_page = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#nextLink')))
            except TimeoutException:
                print('连接超时，章节可能下载不全')
                global changs
                changs = 1
                break
            except AttributeError:
                print ('章节爬取完毕')
                break
        f_write.close()

def main():
    global changs
    try:
        doc = get_doc()
        url = is_items(doc)
        if url:
            get_chapter(url)
    finally:
        browser.close()
        browser.quit()
        if changs == 0:
            print ('下载成功')
        else:
            print ('下载失败')

if __name__ == '__main__':
    main()

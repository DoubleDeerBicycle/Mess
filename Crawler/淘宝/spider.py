from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
from pyquery import PyQuery as pq
import pymongo

client = pymongo.MongoClient('localhost')
db = client['taobao']
#加载谷歌驱动
browser = webdriver.Chrome()
wait = WebDriverWait(browser,10)
def page():
    try:
        #请求链接
        browser.get('https://www.taobao.com')
        #判断输入框是否加载完毕
        element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,'#q'))
        )
        #判断搜索按钮是否可以点击
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_TSearchForm > div.search-button > button')))

        #输入内容
        element.send_keys('美食')
        #点击搜索按钮
        submit.click()
        
        #等待页数加载完毕
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.total')))
        get_products()
        return total.text
    except TimeoutException:
        return page()

def next_page(page_number):
    try:
        element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.form > input')))

        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))

        #清除输入框的内容
        element.clear()

        element.send_keys(page_number)

        submit.click()
        #判断当前页是否是传入进来的数字
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > ul > li.item.active > span'),str(page_number)))
        get_products()
    except TimeoutException:
        next_page(page_number)

def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-itemlist .items .item')))
    
    #获取网页链接
    # url = browser.current_url
    # print (url)
    # 获取网页源代码
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image':item.find('.pic .img').attr('src'),
            'price':item.find('.price').text(),
            'deal':item.find('.deal-cnt').text()[:-3],
            'title':item.find('.title').text(),
            'shop':item.find('.shop').text(),
            'location':item.find('.location').text(),
            'url':item.find('.pic .pic-link').attr('href')
        }
        print (product)
        save_to_mongo(product)
def save_to_mongo(result):
    try:
        if db[MONGO_TABLE_TAOBAO].insert(result):
            print ('存储到MONGODB成功',result)
    except Exception:
        print ('存储到MONGDB失败',result)
def main():
    try:
        total = page()
        
        total = int(re.compile('(\d+)').search(total).group(1))
        for i in range(2,total+1):
            next_page(i)
    finally:
        browser.close()
if __name__ == '__main__':
    main()
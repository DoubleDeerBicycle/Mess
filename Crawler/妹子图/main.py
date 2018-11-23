#!/usr/bin/env python
#-*-conding:utf-8-*-
import requests
import random
import subprocess
import urllib.request
from bs4 import BeautifulSoup
import sys
import threading
from concurrent.futures.process import ProcessPoolExecutor
sys.setrecursionlimit(1000000)

class obj(object):
    """ """
    def __init__(self):
        self.number = 1

    def startpage(self,url,end):
        code = ''
        for i in range(5):
            a = chr(random.randint(97, 122))
            b = random.randint(1, 9)
            uuid = random.choice([a, b])
            code += str(uuid)
        try:
            response = requests.get(url)
            response.encoding = 'utf8'
            html = response.text
            soup = BeautifulSoup(html,'html.parser')
            tag = soup.find(name='div',id='content')
            nexturl = tag.find(name='a').attrs.get('href')
            image = tag.find(name='a').find(name='img')
            imageurl = image.attrs.get('src')
            headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KGTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Content-Type':'image/jpeg',
            'Gost':'img.mmjpg.com',
            'Referer':nexturl,
            'If-None-Match':'59a96b74-%s'%code,
            }
            userinfo = image.attrs.get('alt')
            userinfomation = userinfo.split(' ')[0]
            userinfos = userinfo.replace(' ','')
            getnum = int(imageurl.split('/')[5].split('.')[0])
            #print (userinfo)
            rs = requests.get(imageurl,headers=headers)
            if getnum == 1:
                self.mkdir(userinfomation)
                self.number = 1
            self.getimage(rs.content,userinfomation,userinfos)
            print (imageurl,userinfomation)
            url = nexturl
            self.number += 1
            if nexturl.split('/')[-2] != str(end):
                self.startpage(url,end)
        except Exception as e:
            print (e)

    def getimage(self,url,name,num):
        try:
            iminfo = "G:\\temp\%s\%s.jpg"%(name,num)
            status,resp = subprocess.getstatusoutput('dir %s'%iminfo)
            f = open(iminfo,'wb')
            f.write(url)
            f.close()
        except Exception as e:
            print (e)


    def mkdir(self,dir):
        status,result = subprocess.getstatusoutput("dir G:\\temp\%s"%(dir))
        if status !=0:
            subprocess.Popen("md G:\\temp\%s"%(dir),shell=True)

site = obj()

def main():
    startpage = 1097
    for i in range(41):
        endpage = startpage - 27
        if startpage == 17:
            endpage =0
        url ='http://www.mmjpg.com/mm/%s'%startpage
        t = threading.Thread(target=site.startpage,args=(url,endpage))
        t.start()
        #print (startpage,endpage)
        startpage -= 27
if __name__ == '__main__':
    main()
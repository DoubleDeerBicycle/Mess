import requests,re
import http.cookiejar as cookielib
from PIL import Image


def headers():
    return{
        'referer': 'https://www.zhihu.com/signin',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3371.0 Safari/537.36'
    }
def get_xsrf():
    response = requests.get('https://www.zhihu.com', headers=headers())
    print(response.text)
    return ''

    
def zhihu_login(username, passwd):
    #登录
    if re.search('^1\d{10}',username):
        print('手机号码登录')
        post_url = 'https://www.zhihu.com/login/phone_num'
        post_data = {
            '_xsrf':get_xsrf(),
            'phone_num':username,
            'password':passwd
        }

get_xsrf()
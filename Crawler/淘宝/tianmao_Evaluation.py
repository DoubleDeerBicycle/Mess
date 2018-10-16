import requests
import re
from urllib.parse import urlencode
from requests.exceptions import RequestException
import json
import os
Identity = 0
#返回请求头
def header():
    return{
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3371.0 Safari/537.36'
    }
#请求评论链接
def get_page_html(itemId,currentPage):
    data = {
        'itemId': itemId,
        'spuId': 78348588,
        'sellerId': 2616970884,
        'order': 3,
        'currentPage': currentPage,
        'append': 0,
        'content': 1,
        'tagId': '',
        'posi': '',
        'picture': '',
        'groupId': '',
        'ua': '098#E1hv7pvRvphvU9CkvvvvvjiPPsLv1jEmRssptjivPmPv1jY8RszZ6jnHPscysjE2R2+tvpvhvvvvvUhCvv14cfhvzY147DiQgr/rvpvBUvQLvllavhFKrfm6bD5E3whtvpvhvvvvvUhCvv14cfzSRn147Di9aY/jvpvhvvpvv8wCvvpvvUmmmphvLCvLAQvjcWLWaXkAdcHVafmxfXkfjo2tD7zh58t+m7zhtj7J+3+ulj7OD40OaAuQD7zheTtYvtxr1RoKHkx/1WBlYb8rwZXl+ExreEAtvpvIvvvvvhCvvvvvvUnvphvhU9vv96CvpC29vvm2phCvhhvvvUnvphvppUyCvvOUvvVvayVivpvUvvmvWlDnoeQCvpvVvmvvvhCv2QhvCvvvvvvtvpvhvvvvvv==',
        'needFold': 0,
        '_ksTS': '1538019076846_1712',
        'callback': 'jsonp1713'
    }
    url = 'https://rate.tmall.com/list_detail_rate.htm?'+urlencode(data)
    try:
        response = requests.get(url,headers = header())
        if response.status_code == 200:
            response.encoding = 'utf-8'
            return response.text
    except RequestException:
        print ('请求评论链接失败')
        exit()


def split_html():
    url = input('兄弟，粘贴一下商品网址(仅限天猫)\n')
    if url.count('detail.tmall.com')<=0:
        print ('什么鸡儿玩意儿，你确定这是天猫商品的链接？')
        exit()

    re_url = re.search('.*?&id=(\d+)&',url)
    if re_url != None:
        url = re_url.group(1)
    else:
        print ('MD,你这链接有毒啊!确定一下链接是否完整?')
        exit()
    page = None
    try:
        page = int(input('恩很好，你想爬多少页评论？(一页有二十条评论)\n'))
    except:
        print ('输入数字啊～兄dei')
        exit()
    file_name = input('给你的文件取个名字，我将爬取到的评论写进去\n')
    print ('正在爬取...')
    return [url,page,file_name]

#解析json
def split_json(json_str):
    if  json_str:
        json_start = json_str.index('(')
        re_json = json_str[json_start+1:-1]
        
        json_comments = json.loads(re_json)
        
        #获取其中的评论内容
        rateList = json_comments.get('rateDetail').get('rateList')

        global Identity
        if rateList:
            for comment in rateList:
                appendComment = comment.get('appendComment')
                if appendComment:
                    if comment.get('pics') and appendComment.get('pics'):
                        Identity = 1
                        yield{
                            #评论时间
                            'rateDate':comment.get('rateDate'),
                            #评论内容
                            'rateContent':comment.get('rateContent'),
                            #商品信息
                            'auctionSku':comment.get('auctionSku'),
                            #买家id
                            'displayUserNick':comment.get('displayUserNick'),
                            #买家秀
                            'pics':comment.get('pics'),
                            #追评内容
                            'appendComment':appendComment.get('content'),
                            #追评图片
                            'appendComment_pics':appendComment.get('pics'),
                            #追评时间
                            'commentTime':appendComment.get('commentTime')
                        }
                    elif appendComment.get('pics') and not comment.get('pics'):
                        Identity = 2                        
                        yield{
                            #评论时间
                            'rateDate':comment.get('rateDate'),
                            #评论内容
                            'rateContent':comment.get('rateContent'),
                            #商品信息
                            'auctionSku':comment.get('auctionSku'),
                            #买家id
                            'displayUserNick':comment.get('displayUserNick'),
                            #追评内容
                            'appendComment':appendComment.get('content'),
                            #追评时间
                            'commentTime':appendComment.get('commentTime'),
                            #追评图片
                            'appendComment_pics':appendComment.get('pics')
                        }
                    else:
                        Identity = 5                        
                        yield{
                            #评论时间
                            'rateDate':comment.get('rateDate'),
                            #评论内容
                            'rateContent':comment.get('rateContent'),
                            #商品信息
                            'auctionSku':comment.get('auctionSku'),
                            #买家id
                            'displayUserNick':comment.get('displayUserNick'),
                            #追评内容
                            'appendComment':appendComment.get('content'),
                            #追评时间
                            'commentTime':appendComment.get('commentTime')
                        }
                else:
                    if comment.get('pics'):
                        Identity = 3
                        yield{
                        #评论时间
                        'rateDate':comment.get('rateDate'),
                        #评论内容
                        'rateContent':comment.get('rateContent'),
                        #商品信息
                        'auctionSku':comment.get('auctionSku'),
                        #买家id
                        'displayUserNick':comment.get('displayUserNick'),
                        #买家秀
                        'pics':comment.get('pics')
                        }
                    else:
                        Identity = 4
                        yield{
                        #评论时间
                        'rateDate':comment.get('rateDate'),
                        #评论内容
                        'rateContent':comment.get('rateContent'),
                        #商品信息
                        'auctionSku':comment.get('auctionSku'),
                        #买家id
                        'displayUserNick':comment.get('displayUserNick'),
                        }
def write_file(text_list,file_name):
    global Identity

    dirs = os.getcwd()+'/Crawler/file/tianmao'
    if not os.path.exists(dirs):
        os.makedirs(dirs)
    with open(dirs+'/'+file_name+'.txt','a') as f:
        if Identity == 1:
            f.write('买家id:'+text_list.get('displayUserNick')+'\t评论时间:'+text_list.get('rateDate')+'\t评论内容:'+text_list.get('rateContent')\
            +'\t商品信息:'+text_list.get('auctionSku')+'\t图片:'+str(text_list.get('pics'))+'\t追评时间:'+text_list.get('commentTime')+'\t追评内容:'+\
            text_list.get('appendComment')+'\t追评图片:'+str(text_list.get('appendComment_pics'))+'\n\n'
            )
        if Identity == 3:
            f.write('买家id:'+text_list.get('displayUserNick')+'\t评论时间:'+text_list.get('rateDate')+'\t评论内容:'+text_list.get('rateContent')\
            +'\t商品信息:'+text_list.get('auctionSku')+'\t图片:'+str(text_list.get('pics'))+'\n\n'
            )
        if Identity == 2:
             f.write('买家id:'+text_list.get('displayUserNick')+'\t评论时间:'+text_list.get('rateDate')+'\t评论内容:'+text_list.get('rateContent')\
            +'\t商品信息:'+text_list.get('auctionSku')+'\t追评时间:'+text_list.get('commentTime')+'\t追评内容:'+\
            text_list.get('appendComment')+'\t追评图片:'+str(text_list.get('appendComment_pics'))+'\n\n'
            )
        if Identity == 4:
            f.write('买家id:'+text_list.get('displayUserNick')+'\t评论时间:'+text_list.get('rateDate')+'\t评论内容:'+text_list.get('rateContent')\
            +'\t商品信息:'+text_list.get('auctionSku')+'\n\n'
            )
        if Identity == 5:
             f.write('买家id:'+text_list.get('displayUserNick')+'\t评论时间:'+text_list.get('rateDate')+'\t评论内容:'+text_list.get('rateContent')\
            +'\t商品信息:'+text_list.get('auctionSku')+'\t追评时间:'+text_list.get('commentTime')+'\t追评内容:'+\
            text_list.get('appendComment')+'\n\n'
            )
        f.close()

def main():
    htmls = split_html()
    for page in range(1,htmls[1]+1):
        json_str = get_page_html(htmls[0],page)
        for text_list in split_json(json_str):
            write_file(text_list,htmls[2])
    print ('爬取完毕')
if __name__ == '__main__':
    main()
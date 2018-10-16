import requests
from urllib.parse import urlencode
import re
from requests.exceptions import RequestException
import json
import os
i = 1
#定义请求头，躲避反爬虫机制
def header():
    return {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3371.0 Safari/537.36'
    }

#请求评论链接，获取评论源码
def taobao_get_page_html(auctionNumId,currentPageNum,rateType):
    data = {
        'auctionNumId': auctionNumId,
        'userNumId': 315703723,
        'currentPageNum': currentPageNum,
        'pageSize': 20,
        'rateType': rateType,
        'orderType': 'sort_weight',
        'attribute': '',
        'sku': '',
        'hasSku': 'true',
        'folded': 0,
        'ua': '098#E1hvm9vEvbQvUvCkvvvvvjiPPsSysjiWnLswgjthPmPOtj1hnLsv0jDCP2dp0jnHRphvCvvvphvPvpvhvv2MMQhCvvOvChCvvvmivpvUvvCCE61MIBVEvpvVvpCmpYFwKphv8vvvphvvvvvvvvCj1Qvv9hpvvhNjvvvmjvvvBGwvvvUUvvCj1Qvvv99EvpCW9ViI4Cll5d8reB6QD70fd34AVAilYb8rV8t/LW2vHdoJe5B2AbvqrqpAOH2+Ffmt+3C1oRFE+FuTRogRiNoAdXuKN6qU0EuXjX1touwCvvpvvhHh3QhvCvmvphv=',
        '_ksTS': '1537931690905_1631',
        'callback': 'jsonp_tbcrate_reviews_list'
    }
    url = 'https://rate.taobao.com/feedRateList.htm?'+urlencode(data)
    try:
        response = requests.get(url,headers = header())
        if response.status_code == 200:
            response.encoding = 'utf-8'
            return response.text
        return None
    except RequestException:
        print ('获取评论链接失败')
        exit()

#对评论源码进行json解析
def taobao_get_json(string_json):
    jsons = json.loads(string_json)
    # print (jsons.get('comments'))
    for evaluations in jsons.get('comments'):
        #获取买家id
        userName = evaluations.get('user').get('nick')
        #获取买家评论时间
        userDate = evaluations.get('date')
        #获取买家评论内容
        userText = evaluations.get('content')
        #获取商品价格
        userMoney = None
        if evaluations.get('bidPriceMoney'):
            userMoney = evaluations.get('bidPriceMoney').get('amount')
        #判断买家是否追评，如果追评则获取
        userAdditional = None
        if evaluations.get('append'):
            userAdditional = evaluations.get('append').get('content')
        
        #获取买家购买的商品信息
        userCommodity = evaluations.get('auction').get('sku')
        if userCommodity!='':
            userCommodity = userCommodity.split('&nbsp;&nbsp')
            userCommodity = ','.join(userCommodity)

        yield  {
            'userName':userName,
            'userDate':userDate,
            'userText':userText,
            'userAdditional':userAdditional,
            'userCommodity':userCommodity,
            'userMoney':userMoney
        }
#将解析后的数据写入文件中
def write_to_file(content,file_name):
    global i
    file_dir = os.getcwd()+'/file/淘宝'
    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    #整理字典中的各种数据
    userName = content.get('userName')
    userDate = content.get('userDate')
    userText = content.get('userText')
    userAdditional = content.get('userAdditional')
    userCommodity = content.get('userCommodity')
    userMoney = str(content.get('userMoney'))
    add_if = False
    if userAdditional == None:
        add_if = True
    with open(file_dir+'/'+file_name+'.txt','a',encoding='utf-8') as f:
        if i == 1:
            if add_if:
                f.write('好评----买家id:'+userName+'\t评论时间:'+userDate+'\t评论内容:'+userText+'\t购买的商品:'+userCommodity+'\t购买价格:'+userMoney+'元\n\n')
            else:
                f.write('好评----买家id:'+userName+'\t评论时间:'+userDate+'\t评论内容:'+userText+'\t追评:'+userAdditional+'\t购买的商品:'+userCommodity+'\t购买价格:'+userMoney+'元\n\n')
        if i == 0:
            if add_if:
                f.write('中评----买家id:' + userName + '\t评论时间:' + userDate + '\t评论内容:' + userText + '\t购买的商品:' + userCommodity + '\t购买价格:'+userMoney+'元\n\n')
            else:
                f.write('中评----买家id:' + userName + '\t评论时间:' + userDate + '\t评论内容:' + userText + '\t追评:' + userAdditional + '\t购买的商品:' + userCommodity + '\t购买价格:'+userMoney+'元\n\n')
        if i == -1:
            if add_if:
                f.write('差评----买家id:'+userName+'\t评论时间:'+userDate+'\t评论内容:'+userText+'\t购买的商品:'+userCommodity+'\t购买价格:'+userMoney+'元\n\n')
            else:
                f.write('差评----买家id:'+userName+'\t评论时间:'+userDate+'\t评论内容:'+userText+'\t追评:'+userAdditional+'\t购买的商品:'+userCommodity+'\t购买价格:'+userMoney+'元\n\n')
        f.close()
def main():
    commodityUrl = input('劳烦你粘贴一下商品链接\n')
    if commodityUrl.count('item.taobao')>0:
        try:
            page = int(input('兄弟，需要爬取多少页评论?(一页有二十条评论)\n'))
        except ValueError:
            print ('听着，为什么你就不能输入一下纯粹的数字呢？')
            exit()
        file_name = input('劳烦你输入一个文件名，我好将数据写入进去\n')
        print ('正在尝试爬取...')
        reCommodityUrl = re.search('&id=(\d+)&',commodityUrl).group(1)
        string_json = None
        global i
        while i==1 or i==0 or i==-1:
            for pgnum in range(1,page+1):
                string_json = taobao_get_page_html(reCommodityUrl,pgnum,i)
                if string_json != None:
                    #对返回的源码进行截取，获取json串
                    mark_num = string_json.index('(')
                    split_string_json = string_json[mark_num+1:-1]
                    textLists = taobao_get_json(split_string_json)
                    if textLists != None:
                        for textList in textLists:
                            write_to_file(textList,file_name) 
            i-=1
        print ('爬取成功,恭喜你，兄弟')
    else:
        print ('我想,这应该不是淘宝商品的链接(暂不支持天猫)')
if __name__ == '__main__':
    main()


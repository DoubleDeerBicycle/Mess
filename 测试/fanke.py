import requests
import re
from pyquery import PyQuery as pq


class FanKe():
    def __init__(self):
        self.index_url = 'http://downcoat.vancl.com/#ref=hp-hp-head-nav_2-v:n'

    def main(self):
        try:
            response = requests.get(self.index_url)
            if response.status_code == 200:
                doc = pq(response.text)
                pq_ul = doc.find('ul.shirts-product-list')
                if pq_ul:
                    pq_titles = pq_ul.find('li a.product-img').items()
                    pq_price = pq_ul.find('span.sprice').items()
                    for title, price in zip(pq_titles, pq_price):
                        print(title.attr('title')+':\t', end='')
                        print(re.search('.*?(\d+.*)', price.text()).group(1))
        except Exception as e:
            print(e)

my_crawl = FanKe()
my_crawl.main()
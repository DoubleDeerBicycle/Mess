import sys,os
from scrapy.cmdline import execute
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(['scrapy', 'crawl','zhihu'])
# print(os.path.dirname(os.path.abspath(__file__)))
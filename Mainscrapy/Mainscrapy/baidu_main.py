import sys
import os
from scrapy.cmdline import execute


def get_baidu_key_words():
    """Start the program to get key-value of  from baike.baidu.com
    Every result will save in Mysql database by django model
    """
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    execute(['scrapy', 'crawl', 'baidu_spider'])


get_baidu_key_words()

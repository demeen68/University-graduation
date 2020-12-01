import sys
import os
from scrapy.cmdline import execute
import subprocess

username = 'nhmanager'
password = 'mynhmanager'
database = 'nhdata'


def start_scrapy():
    """Start a scrapy and get news from news.baidu.com
    """
    try:
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        # subprocess.call("pwd",shell=True)
        # execute(['scrapy', 'crawl', 'xinwen_spider'])
        execute(['scrapy', 'crawl', 'xinwen_spider'])
    except Exception as e:
        print(e)


start_scrapy()

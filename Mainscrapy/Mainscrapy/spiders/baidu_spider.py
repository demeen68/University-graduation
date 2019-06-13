# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider
from Mainscrapy.items import BaiduItem
from urllib.request import unquote
from urllib.parse import urljoin
from scrapy.http import Request
import scrapy
import pickle
import os


class BaiduSpiderSpider(CrawlSpider):
    """Use Scrapy structure and get the key-value pairs of title and highlight key words
    """
    name = "baidu_spider"
    allowed_domains = ["baike.baidu.com/"]
    ignore_words = []
    custom_settings = {
        'DEPTH_LIMIT': 10,
        # Basically , this code need to save temporary schedule
        # 'JOBDIR': '~/jobdir/baidu_spider_jobdir'
    }

    def start_requests(self):
        """Get words which should to be ignored and set init url
        This project we get key words form '肥胖'
        """
        self.ignore_words = pickle.load(
            open(os.path.dirname(__file__) + '/../../../Mainweb/extra_apps/extra_motion/baidu_ignore.pkl', 'rb'))
        yield scrapy.Request(
            'https://baike.baidu.com/item/%E8%82%A5%E8%83%96',
            self.parse, dont_filter=True)

    def parse(self, response):
        """Analyze the html and extract key words from html web page

        :param response:html contents
        """
        url = response.url.replace('https://baike.baidu.com/item/', '')
        fa_content = unquote(url, encoding='utf-8')

        whole_content = response.css('.main-content div.para')
        all_a_label = whole_content.css('a[target]').css('a[href]')
        all_text = all_a_label.css('::text').extract()
        for content in all_text:
            content = content.strip()
            if content is not '' and len(content) < 10:
                # todo next url
                con = content.split('/')[0]
                fa_con = fa_content.split('/')[0]
                if con not in self.ignore_words:
                    item = BaiduItem()
                    item['fa_content'] = fa_con
                    item['content'] = con
                    yield item
                    next_url = '/item/' + content
                    next_url = urljoin(response.url, next_url)
                    yield Request(url=next_url, callback=self.parse, dont_filter=True)

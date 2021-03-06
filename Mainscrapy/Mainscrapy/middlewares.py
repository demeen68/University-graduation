# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent
from selenium import webdriver
from scrapy.http import HtmlResponse
import time


class MainscrapySpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomUserAgentMiddleware(object):
    """make User-Agent in a data package is random in case baidu drop the package
    """

    def __init__(self, crawler):
        super(RandomUserAgentMiddleware, self).__init__()
        self.ua = UserAgent()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', self.ua.random)


class HandlessMiddleware(object):

    def __init__(self):
        super(HandlessMiddleware, self).__init__()
        option = webdriver.ChromeOptions()
        # self.ua = UserAgent()

        option.add_argument('--disable-gpu')
        option.add_argument('lang=zh_CN.UTF-8')
        # option.add_argument(
        #     'user-agent=' + self.ua.random)
        # option.add_argument('headless')
        prefs = {
            "profile.managed_default_content_settings.images": 2,  # 禁止加载图片
            # 'permissions.default.stylesheet': 2,  # 禁止加载css
        }
        option.add_experimental_option("prefs", prefs)
        self.browser = webdriver.Chrome(chrome_options=option)
        self.browser.implicitly_wait(10)

    def process_request(self, request, spider):
        # self.browser.get(request.url)

        print("NEW PAGE GET : " + request.url)
        self.browser.get(request.url)
        time.sleep(10)
        return HtmlResponse(url=self.browser.current_url, body=self.browser.page_source, encoding="utf-8",
                            request=request)

# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy_app.models import BaiduContentModel, NewsListModel, NewsModel
from scrapy_djangoitem import DjangoItem


class BaiduItem(DjangoItem):
    """Each words will save in Mysql database by django_model
    """
    django_model = BaiduContentModel


class news_listItem(DjangoItem):
    django_model = NewsListModel


class newsItem(DjangoItem):
    django_model = NewsModel

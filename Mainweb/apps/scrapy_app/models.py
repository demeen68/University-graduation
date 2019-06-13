from django.db import models
from datetime import datetime


class BaiduContentModel(models.Model):
    """Save content between key word and other relative key words from baike.baidu.com
    """
    fa_content = models.CharField(max_length=255, default='')
    content = models.CharField(max_length=255)


class NewsListModel(models.Model):
    """Actually this model have no use , it is just used as the originator of the project to debug
    """
    url = models.CharField(max_length=255, primary_key=True)
    key_words = models.CharField(max_length=255, default='')
    author_relative_time = models.CharField(max_length=255)
    time = models.DateField(default=datetime.now)


class NewsModel(models.Model):
    """Save news details

    key_words : this news was saved by which key word
    motion : Quantitative the text and use different dimensions to express
    time : this news create time
    """
    url = models.CharField(max_length=255, primary_key=True)
    key_words = models.CharField(max_length=255, default='')
    title_key = models.CharField(max_length=300, default='')
    motion = models.CharField(max_length=250, default='')
    time = models.DateField(default=datetime.now)


class NeedTitleModel(models.Model):
    """This model means which news with this key words need to get from baidu news .
    """
    key_words = models.CharField(max_length=255, primary_key=True)
    add_user = models.CharField(max_length=255, default='')
    create_time = models.DateField(default=datetime.now)
    has_get_past_news = models.BooleanField(default=False)
    has_send_email = models.BooleanField(default=False)


class MotionModel(models.Model):
    """ Save motion of the title
    """
    title = models.CharField(max_length=255)
    positive_rate = models.CharField(max_length=255)
    news_number = models.CharField(max_length=255)
    date_time = models.DateField()


class OfflineWord2vecModel(models.Model):
    key1 = models.CharField(max_length=255)
    key2 = models.CharField(max_length=255)


class SuggestionModel(models.Model):
    """Send user some suggestion
    """
    title = models.CharField(max_length=255,default='')
    # suggestion save html tag and content directly, and sprite by ';'
    suggestion = models.TextField(default='')

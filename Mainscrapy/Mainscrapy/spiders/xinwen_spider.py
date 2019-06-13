# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider
from Mainscrapy.items import news_listItem, newsItem
from scrapy.http import Request
import scrapy
import jieba
import jieba.analyse
import pickle
from datetime import date
import MySQLdb
import os


class BaiduSpiderSpider(CrawlSpider):
    """Get news from news.baidu.com
    """
    name = "xinwen_spider"
    allowed_domains = ["news.baidu.com"]
    stopwords = []

    custom_settings = {
        'HTTPERROR_ALLOWED_CODES': [302, 301],
    }

    def start_requests(self):
        # get stopwords to analyze
        self.stopwords = pickle.load(
            open(os.path.dirname(__file__) + '/../../../Mainweb/extra_apps/extra_motion/stopwords.pkl', 'rb'))
        # get web list

        # todo test cron
        print("Get CRON")

        need_titles = get_key_words()
        for need_tit in need_titles:
            title = str(need_tit[0])
            has_get_past_news = int(need_tit[1])
            if has_get_past_news:
                # page2:
                # http://news.baidu.com/ns?word=%27%20%E5%87%8F%E8%82%A5%20%27&pn=20&cl=2&ct=0&tn=news&rn=20&ie=utf-8&bt=0&et=0
                # page3:
                # http://news.baidu.com/ns?word=%27%20%E5%87%8F%E8%82%A5%20%27&pn=40&cl=2&ct=0&tn=news&rn=20&ie=utf-8&bt=0&et=0

                will_url = 'http://news.baidu.com/ns?word=' + title + \
                           '&pn=0&cl=2&ct=0&tn=news&rn=20&ie=utf-8&bt=0&et=0&clk=sortbytime'
                yield scrapy.Request(will_url, callback=self.parse, dont_filter=True, meta={
                    'key_words': title,
                    'circle': 0,
                })
            else:
                for i in range(20):
                    will_url = str('http://news.baidu.com/ns?word=' + title + '&pn=' + str(
                        20 * i) + '&cl=2&ct=0&tn=news&rn=20&ie=utf-8&bt=0&et=0&clk=sortbytime')
                    yield scrapy.Request(will_url, callback=self.parse, dont_filter=True, meta={
                        'key_words': title,
                        'circle': i,
                    })
                change_has_get_past(title)

    def parse(self, response):
        """Get definite URL from news lists.
        Each news list have 20 news.

        :param response: News list web page
        """
        circle = response.meta['circle']
        for i in range(30):
            # url_help_str can get the id of the news with <div>
            url_help_str = '#' + str(circle * 20 + i + 1)
            news_urls_div = response.css(url_help_str)
            # test_news_urls_div = response.css(url_help_str).extract()
            news_url = news_urls_div.css('a::attr(href)').extract_first()
            if news_url is None:
                continue
            key_words = response.meta['key_words']
            if check_url(news_url):
                key_words_exist = have_key_word(news_url, key_words)
                if key_words_exist:
                    continue
                else:
                    add_title_in_db(news_url, key_words, key_words_exist)
                    continue
            else:
                author = str(news_urls_div.css('p.c-author::text').extract_first())
                author = "".join(author.split())
                if author[-1] == '前':
                    time = date.today()
                else:
                    this_time = author[-16:-5]
                    time = date(int(this_time[0:4]), int(this_time[5:7]), int(this_time[8:10]))
                yield Request(url=news_url, callback=self.analyze_news, dont_filter=True, meta={
                    'key_words': key_words,
                    'time': time,
                })
                news_list_item = news_listItem()
                news_list_item['url'] = news_url
                news_list_item['key_words'] = key_words
                news_list_item['author_relative_time'] = author
                news_list_item['time'] = time
                yield news_list_item

    def analyze_news(self, response):
        """Analyze news from different news website.
        Acturally , we can not get desired result each time since different news website have different layout.So
        we choice <p> tags and think it contains news content by default. Next we will find the number of
        characters it has ,if it is less than 50 , this news will be delete and won't added to the statistics.

        :param response:a news web page
        """
        # Get segment
        p_content_css = response.css('p::text')
        p_content = p_content_css.extract()
        content_s = []
        for content in p_content:
            segment = jieba.lcut(content.strip())
            if len(segment) > 1 and segment != '\r' and segment != '\n' and segment != ' ' and segment != '\t':
                content_s.append(segment)
        content_list = drop_stopwords(content_s, self.stopwords)
        # Some reporter dont write news in <p>
        if len(content_list) > 50:
            # Get motion dict
            motion_dic = pickle.load(
                open(os.path.dirname(__file__) + '/../../../Mainweb/extra_apps/extra_motion/motion_dic.pkl',
                     'rb'))
            main_motion = {}
            positive_number = 0
            pos_neg_number = 0
            for words in content_list:
                motion_list = motion_dic.get(words, '')
                if motion_list:
                    # check if we have got this motion
                    if motion_list[0] == 'good' or motion_list[0] == 'happy':
                        positive_number += float(motion_list[1])
                    pos_neg_number += float(motion_list[1])
                    if main_motion.get(motion_list[0]):
                        main_motion[motion_list[0]] += float(motion_list[1])
                    else:
                        main_motion.update({motion_list[0]: float(motion_list[1])})
            motion_str = ''
            for key, value in main_motion.items():
                motion_str += ("%s,%s," % (key, str(value)))
            time = response.meta['time']
            key_words = response.meta['key_words']
            # Save url and all html
            if motion_str is not '':
                save_motion(key_words, time, (positive_number / pos_neg_number) * 100)
                # if motion is not '' , then analyze title_keys
                content_s = "".join(content_list).strip()
                title_keys = jieba.analyse.extract_tags(content_s, topK=7, withWeight=False)  # get 8 keys
                title_keys = ','.join(title_keys)
                news_item = newsItem()
                news_item['url'] = response.url
                news_item['key_words'] = key_words
                news_item['title_key'] = title_keys
                news_item['motion'] = motion_str
                news_item['time'] = time
                yield news_item


def save_motion(title, time, potivite_rate):
    """ Save the emotion data of text which has been quantified and statistic.

    :param title: The title of the news.
    :param time:  The timing of the news release.
    :param potivite_rate: potivite words weight / all words motion weight
    """
    db = MySQLdb.connect("localhost", " 用户名", "密码", "数据库名", charset='utf8')
    cursor = db.cursor()
    cursor.execute(
        "SELECT `positive_rate`,`news_number`,`id` FROM `scrapy_app_motionmodel` WHERE `title`=%s AND `date_time`=%s;",
        [title, time])
    posrate_number = cursor.fetchall()
    if posrate_number:
        # update the data
        old_positive_rate = float(posrate_number[0][0])
        news_number = float(posrate_number[0][1])
        now_rate = (old_positive_rate * news_number + potivite_rate) / float(news_number + 1)
        now_rate = float('%.2f' % now_rate)
        db_str = "UPDATE `scrapy_app_motionmodel` SET `positive_rate`=%s, `news_number`=%s WHERE `id`=%s;"
        cursor.execute(db_str, [now_rate, news_number + 1, int(posrate_number[0][2])])
        db.commit()
    else:
        # first time to add potivite rate
        db_str = "INSERT INTO `scrapy_app_motionmodel` (`title`, `positive_rate`, `news_number`,`date_time`) VALUES (%s, %s, %s,%s);"
        cursor.execute(db_str, [title, potivite_rate, 1, time])
        db.commit()
    db.close()


def drop_stopwords(contents, stopwords):
    contents_clean = []
    for line in contents:
        line_clean = []
        for word in line:
            if word in stopwords:
                continue
            line_clean.append(word)
        contents_clean.extend(line_clean)
    return contents_clean


def get_key_words():
    db = MySQLdb.connect("localhost", " 用户名", "密码", "数据库名", charset='utf8')
    cursor = db.cursor()
    cursor.execute("SELECT key_words,has_get_past_news FROM scrapy_app_needtitlemodel;")
    key_words = cursor.fetchall()
    db.close()
    return key_words


def change_has_get_past(key_words):
    db = MySQLdb.connect("localhost", " 用户名", "密码", "数据库名", charset='utf8')
    cursor = db.cursor()
    db_str = "UPDATE `scrapy_app_needtitlemodel` SET `has_get_past_news`=%s WHERE `key_words`=%s ;"
    cursor.execute(db_str, (1, key_words))
    db.commit()
    db.close()


# check if db has this key word
def have_key_word(url, key_words):
    db = MySQLdb.connect("localhost", " 用户名", "密码", "数据库名", charset='utf8')
    db_str = "select key_words from scrapy_app_newsmodel where FIND_IN_SET(%s, key_words) and url=%s;"
    cursor = db.cursor()
    cursor.execute(db_str, [key_words, url])
    key_words_exist = cursor.fetchall()
    db.close()
    return key_words_exist


def check_url(url):
    db = MySQLdb.connect("localhost", " 用户名", "密码", "数据库名", charset='utf8')
    db_str = "select url from scrapy_app_newsmodel where url=%s"
    cursor = db.cursor()
    cursor.execute(db_str, [url])
    result = cursor.fetchall()
    db.close()
    if result:
        return True
    else:
        return False


# maybe this method have some bugs
def add_title_in_db(url, new_key_word, key_words_exsit):
    tup_str = ''
    for t in key_words_exsit:
        tup_str = tup_str + t[0] + ","
    db = MySQLdb.connect("localhost", " 用户名", "密码", "数据库名", charset='utf8')
    cursor = db.cursor()
    db_str = "UPDATE `scrapy_app_newsmodel` SET `key_words`=%s WHERE `url`=%s;"
    cursor.execute(db_str, (key_words_exsit + new_key_word, url))
    db.commit()
    db.close()

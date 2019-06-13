# -*- coding: utf-8 -*-
import sys
import os
import django

BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
PRO_ROOT = os.path.dirname(BASE_DIR)  # 两个项目共同的根目录

sys.path.append(os.path.join(PRO_ROOT, 'Mainscrapy'))
sys.path.append(os.path.join(BASE_DIR, 'Mainscrapy'))
# sys.path.append(os.path.join(PRO_ROOT, '../../../..'))
sys.path.append(os.path.join(PRO_ROOT, 'Mainweb'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'Mainweb.settings'
django.setup()

# LOG_LEVEL = 'ERROR'
# Scrapy settings for Mainscrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# COOKIES_ENABLED = False
BOT_NAME = 'Mainscrapy'
FEED_EXPORT_ENCODING = 'utf-8'
SPIDER_MODULES = ['Mainscrapy.spiders']
NEWSPIDER_MODULE = 'Mainscrapy.spiders'
# DUPEFILTER_DEBUG = True  # more log we can see
# DEPTH_LIMIT = 10  # how deep we need to get
HTTPERROR_ALLOWED_CODES = [302, 301]
# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'Mainscrapy (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
AUTOTHROTTLE_ENABLED = True  # auto limit
DOWNLOAD_DELAY = 5  # auto download
# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 0.25
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'Mainscrapy.middlewares.MainscrapySpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.useragent.UsserAgentMiddleware': None,
    'Mainscrapy.middlewares.RandomUserAgentMiddleware': 200,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'Mainscrapy.pipelines.MainscrapyPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html

# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

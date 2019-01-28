# -*- coding: utf-8 -*-

# Scrapy settings for shopee_scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'shopee_scraper'

SPIDER_MODULES = ['shopee_scraper.spiders']
NEWSPIDER_MODULE = 'shopee_scraper.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'shopee_scraper (+http://www.yourdomain.com)'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = '"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# LOG_STDOUT = True
# LOG_LEVEL = 'INFO'

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
#    'shopee_scrapper.middlewares.ShopeeScrapperSpiderMiddleware': 543,
}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
   # 'shopee_scrapper.middlewares.ShopeeScrapperDownloaderMiddleware': 543,
}

DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

# Splash settings
SPLASH_URL = 'https://kncbase5-splash.scrapinghub.com'     # Splash instance URL from Scrapy Cloud
SPLASH_APIKEY = '83261d30c0d946f3bbaf7072bc4bff29'  # Your API key for the Splash instance hosted on Scrapy Cloud
# CRAWLERA_APIKEY = '9de8b5d8f4f149c99392853999441fca'  # Your crawlera API key
CRAWLERA_APIKEY = '2fbf026381674294b5e4c58db42201f6'  # Your crawlera API key
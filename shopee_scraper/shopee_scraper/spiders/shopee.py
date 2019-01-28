# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
import json
import re
from datetime import date
import requests
from pkgutil import get_data
from w3lib.http import basic_auth_header


class ShopeeSpider(scrapy.Spider):
    name = 'shopee'
    allowed_domains = ['shopee.co.id']
    start_urls = ["https://shopee.co.id/"]


    # custom_settings = {"LOG_FILE": "shopee_{}.log".format(str_today),
    #                    "LOG_LEVEL": 'INFO',
    #                    "DOWNLOAD_DELAY": 0.5
    #                    }

    def __init__(self, *args, **kwargs):
        str_today = date.today().strftime("%Y%m%d")
        try:
            self.scraped_urls = open("Scraped_URLs.txt", "r", encoding="utf-8").read().split("\n")
        except:
            self.scraped_urls = []
        self.scraped_file = open("Scraped_URLs.txt", "a", encoding="utf-8")

        self.log_file = open("shopee_{}.log".format(str_today), "a", encoding="utf-8")

        self.LUA_SOURCE = get_data(
            'shopee_scraper', 'scripts/crawlera.lua'
        ).decode('utf-8')
        super(ShopeeSpider, self).__init__(*args, **kwargs)

    def __make_category_url(self, category_main):
        suffix = re.sub("[^0-9a-zA-Z]+", "-", category_main["display_name"])
        category_url = "https://shopee.co.id/{}-cat.{}".format(suffix, category_main["catid"])
        return category_main["name"], category_url

    def start_requests(self):
        start_url = 'https://shopee.co.id/api/v1/category_list/'
        yield scrapy.Request(start_url, self.category_urls)

    def category_urls(self, response):
        categories = json.loads(response.body.decode("utf-8"))
        max_pagenum = 100
        for category in categories[::-1]:
            category_name, url = self.__make_category_url(category["main"])
            print(category_name, url)
            for sub in category["sub"]:
                sub_category = sub["name"]
                sub_catid = sub["catid"]
                for sub_sub in sub["sub_sub"]:
                    sub_sub_category = sub_sub["name"]
                    sub_sub_catid = sub_sub["catid"]
                    sub_sub_category_display = sub_sub["display_name"]

                    for pagenum in range(max_pagenum):
                        url_page = url + ".{sub_catid}.{sub_sub_catid}?page={pagenum}&sortBy=sales".format(
                            sub_catid=sub_catid,
                            sub_sub_catid=sub_sub_catid,
                            pagenum=pagenum)
                        if url_page in self.scraped_urls:
                            logTxt = "(Already Scraped URL Page)\t\t{}".format(url_page)
                            self.write_log(logTxt)
                            continue

                        yield SplashRequest(
                            url=url_page,
                            callback=self.parse,
                            args={
                                'wait': 10,
                                'images_enabled': False,
                                "timeout": 60,
                                'lua_source': self.LUA_SOURCE,
                                'crawlera_user': self.settings['CRAWLERA_APIKEY'],
                            },
                            endpoint='render.har',  # optional; default is render.html
                            # endpoint='execute',  # optional; default is render.html
                            splash_headers={
                                'Authorization': basic_auth_header(self.settings['SPLASH_APIKEY'], ''),
                            },
                            cache_args=['lua_source'],
                            meta={"category_name": category_name,
                                  "sub_category": sub_category,
                                  "sub_sub_category_displayname": sub_sub_category_display,
                                  "sub_sub_category": sub_sub_category,
                                  "sub_catid": sub_catid,
                                  "sub_sub_catid": sub_sub_catid,
                                  "pagenum": pagenum,
                                  "url_page": url_page
                                  }
                        )

    def parse(self, response):
        entries = response.data["log"]["entries"]
        sub_sub_cat_name = response.meta["sub_sub_category_displayname"]
        url_page = response.meta["url_page"]
        self.append_url_page(url_page)

        url = None
        for entry in entries:
            request = entry["request"]
            sub_sub_cat_name = re.sub("[^0-9a-zA-Z]+", "-", sub_sub_cat_name)
            if 'https://shopee.co.id/api/v2/search_items/' in request["url"] and sub_sub_cat_name in request["url"]:
                headers = {header["name"]: header["value"] for header in request["headers"]}
                url = request["url"]
                break
        if url:
            resp = requests.get(url,
                                headers=headers,
                                timeout=360,
                                )
            items = json.loads(resp.text)["items"]
            if len(items) == 0:
                return


            logTxt = "(Scraped URL Page)\t{}".format(url_page)
            self.write_log(logTxt)
            logTxt = "\t{} items scraped\t, {}".format(len(items), url)
            self.write_log(logTxt)
            for item in items:

                yield {
                    "itemid": item["itemid"],
                    "rating_star": item["item_rating"]["rating_star"],
                    "name": item["name"],
                    "price": item["price"],
                    "shopid": item["shopid"],
                    "shopee_verified": item["shopee_verified"],
                    "sold": item["sold"],
                    "catid": item["catid"],
                    "sub_catid": response.meta["sub_catid"],
                    "sub_sub_catid": response.meta["sub_sub_catid"],
                    "brand": item["brand"],
                    "is_official_shop": item["is_official_shop"],
                    "view_count": item["view_count"],
                    "stock": item["stock"],
                    "category": response.meta["category_name"],
                    "sub_category": response.meta["sub_category"],
                    "sub_sub_category": response.meta["sub_sub_category"],
                    "pagenum": response.meta["pagenum"]
                }
        else:
            logTxt = "(Scraped URL Page)\t{}".format(url_page)
            self.write_log(logTxt)
            logTxt = "\t{} items scraped\t, {}".format(0, url)
            self.write_log(logTxt)

    def write_log(self, logTxt):
        self.log_file.write(logTxt+"\n")
        self.log_file.flush()
        print(logTxt)

    def append_url_page(self, url_page):
        self.scraped_urls.append(url_page)
        self.scraped_file.write(url_page + "\n")
        self.scraped_file.flush()

if __name__ == '__main__':
    from scrapy import cmdline
    from datetime import date
    import pandas as pd
    from shopee_scraper.settings import *

    cmdline.execute("scrapy crawl shopee -o {}".format(LOG_FILE_PRODUCT).split())

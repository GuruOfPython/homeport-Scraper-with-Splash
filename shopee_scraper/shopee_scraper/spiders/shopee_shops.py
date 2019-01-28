# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
import pandas as pd
import json
import requests
import re
from datetime import date
import time
from pkgutil import get_data
from w3lib.http import basic_auth_header
from shopee_scraper.settings import *

class ShopeeShopsSpider(scrapy.Spider):
    name = 'shopee_shops'
    # str_today = "20180629"
    # date.today().strftime("%Y%m%d")
    allowed_domains = ['shopee.co.id']
    # custom_settings = {'CONCURRENT_REQUESTS': "32",
    #                    "LOG_FILE": "shopee_shops_{}.log".format(str_today)}

    def __init__(self, *args, **kwargs):

        str_today = date.today().strftime("%Y%m%d")
        self.log_file = open("shopee_shops_{}.log".format(str_today), "a", encoding="utf-8")

        self.LUA_SOURCE = get_data(
            'shopee_scraper', 'scripts/crawlera.lua'
        ).decode('utf-8')
        super(ShopeeShopsSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        url = 'https://shopee.co.id/%F0%9F%92%95Celana-Pendek-Pria-i.8497368.57564317'
        yield SplashRequest(url, self.extract_headers,
                            args={
                                'wait': 10,
                                'images_enabled': False,
                                "timeout": 60,
                                'lua_source': self.LUA_SOURCE,
                                'crawlera_user': self.settings['CRAWLERA_APIKEY'],
                            },
                            endpoint='render.har',  # optional; default is render.html
                            splash_headers={
                                'Authorization': basic_auth_header(self.settings['SPLASH_APIKEY'], ''),
                            },
                            cache_args=['lua_source'],
                            )

    def extract_headers(self, response):
        entries = response.data["log"]["entries"]
        url = None
        for entry in entries:
            request = entry["request"]
            if 'https://shopee.co.id/api/v1/item_detail/' in request["url"]:
                headers = {header["name"]: header["value"] for header in request["headers"]}
                try:
                    csrftoken = re.findall("csrftoken=(.*);.*;", headers["Cookie"])[0]
                    headers["x-csrftoken"] = csrftoken
                    url = request["url"]
                    break
                except Exception as e:
                    self.logger.error(e)
        if url:
            # shopids = list(map(int, pd.read_json("shopee_{}.json".format(self.str_today))["shopid"].unique()))
            shopids = list(map(int, pd.read_json(LOG_FILE_PRODUCT)["shopid"].unique()))
            n = len(shopids)
            chunk_size = 400
            chunks = n // chunk_size
            for i in range(chunks + 1):
                ids = shopids[i * chunk_size:(i + 1) * chunk_size]
                shop_url = "https://shopee.co.id/api/v1/shops/"
                self.logger.info("retrieving {} ids".format(chunk_size * i))

                logTxt = "retrieving {} ids".format(chunk_size * i)
                self.write_log(logTxt)

                resp = requests.post(shop_url, data=json.dumps({"shop_ids": ids}), headers=headers)
                js = json.loads(resp.text)
                self.logger.info("shop counts: {}".format(len(js)))

                logTxt = "shop counts: {}".format(len(js))
                self.write_log(logTxt)

                for item in js:
                    yield item
                time.sleep(5)

    def write_log(self, logTxt):
        self.log_file.write(logTxt+"\n")
        self.log_file.flush()
        print(logTxt)

if __name__ == '__main__':
    from scrapy import cmdline
    from datetime import date
    import pandas as pd
    from shopee_scraper.settings import *

    cmdline.execute("scrapy crawl shopee_shops -o {}".format(LOG_FILE_SHOP).split())
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field


class ProductInfoItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    itemid = Field()
    rating_star = Field()
    name = Field()
    price = Field()
    shopid = Field()
    shopee_verified = Field()
    sold = Field()
    catid = Field()
    sub_catid = Field()
    sub_sub_catid = Field()
    brand = Field()
    is_official_shop = Field()
    view_count = Field()
    stock = Field()
    category = Field()
    sub_category = Field()
    sub_sub_category = Field()
    pagenum = Field()


class ShopInfoItem(Item):
    username = Field()
    rating_normal = Field()
    followed = Field()
    following_count = Field()
    userid = Field()
    is_free_shipping = Field()
    shopid = Field()
    rating_bad = Field()
    preparation_time = Field()
    portrait = Field()
    is_shopee_verified = Field()
    show_low_fulfillment_warning = Field()
    item_count = Field()
    show_official_shop_label = Field()
    follower_count = Field()
    enable_display_unitno = Field()
    status = Field()
    is_blocking_owner = Field()
    description = Field()
    rating_good = Field()
    is_semi_inactive = Field()
    shop_covers = Field()
    chat_disabled = Field()
    response_time = Field()
    ctime = Field()
    response_rate = Field()
    disable_make_offer = Field()
    name = Field()
    cover = Field()
    total_avg_star = Field()
    free_shipping_min_total = Field()
    holiday_mode_on = Field()
    place = Field()
    last_active_time = Field()

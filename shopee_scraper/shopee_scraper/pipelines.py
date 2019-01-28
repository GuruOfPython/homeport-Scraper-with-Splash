# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3 as lite


class ShopeeScraperPipeline(object):
    def __init__(self):
        self.setupDBCon()
        self.createTables()

    def createTables(self):
        # self.dropProductTable()
        # self.dropShopTable()

        self.createProductTable()
        self.createShopTable()

    def setupDBCon(self):
        self.con = lite.connect('shopee.db')
        self.cur = self.con.cursor()

    def dropProductTable(self):
        self.cur.execute("DROP TABLE IF EXISTS Product")

    def dropShopTable(self):
        self.cur.execute("DROP TABLE IF EXISTS Shop")

    def createProductTable(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS Product(id INTEGER PRIMARY KEY NOT NULL, \
    		itemid INT, \
    		rating_star REAL, \
    		name TEXT, \
    		price INT, \
    		shopid INT, \
    		shopee_verified BOOLEAN, \
    		sold INT, \
    		catid INT, \
    		sub_catid INT, \
    		sub_sub_catid INT, \
    		brand TEXT, \
    		is_official_shop BOOLEAN, \
    		view_count INT, \
    		stock INT, \
    		category TEXT, \
    		sub_category TEXT, \
    		sub_sub_category TEXT, \
    		pagenum INT \
    		)")

    def createShopTable(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS Shop(id INTEGER PRIMARY KEY NOT NULL, \
    		username TEXT, \
    		rating_normal INT, \
    		followed BOOLEAN, \
    		following_count INT, \
    		userid INT, \
    		is_free_shipping BOOLEAN, \
    		shopid INT, \
    		rating_bad INT, \
    		preparation_time INT, \
    		portrait TEXT, \
    		is_shopee_verified BOOLEAN, \
    		show_low_fulfillment_warning BOOLEAN, \
    		item_count INT, \
    		show_official_shop_label BOOLEAN, \
    		follower_count INT, \
    		enable_display_unitno BOOLEAN, \
    		status INT, \
    		is_blocking_owner BOOLEAN, \
    		description TEXT, \
    		rating_good INT, \
    		is_semi_inactive BOOLEAN, \
    		shop_covers TEXT, \
    		chat_disabled BOOLEAN, \
    		response_time INT, \
    		ctime INT, \
    		response_rate TEXT, \
    		disable_make_offer INT, \
    		name TEXT, \
    		cover TEXT, \
    		total_avg_star REAL, \
    		free_shipping_min_total REAL, \
    		holiday_mode_on BOOLEAN, \
    		place TEXT, \
    		last_active_time BIGINT \
            )")

    def process_item(self, item, spider):
        if spider.name == "shopee":
            self.storeProductInfoInDb(item)
        if spider.name == "shopee_shops":
            self.storeShopInfoInDb(item)
        return item

    def storeProductInfoInDb(self, item):
        itemid = item.get('itemid', '')
        rating_star = item.get('rating_star', '')
        name = item.get('name', '')
        price = item.get('price', '')
        shopid = item.get('shopid', '')
        shopee_verified = item.get('shopee_verified', '')
        sold = item.get('sold', '')
        catid = item.get('catid', '')
        sub_catid = item.get('sub_catid', '')
        sub_sub_catid = item.get('sub_sub_catid', '')
        brand = item.get('brand', '')
        is_official_shop = item.get('is_official_shop', '')
        view_count = item.get('view_count', '')
        stock = item.get('stock', '')
        category = item.get('category', '')
        sub_category = item.get('sub_category', '')
        sub_sub_category = item.get('sub_sub_category', '')
        pagenum = item.get('pagenum', '')

        self.cur.execute("INSERT INTO Product(\
        			itemid, \
                    rating_star, \
                    name, \
                    price, \
                    shopid, \
                    shopee_verified, \
                    sold, \
                    catid, \
                    sub_catid, \
                    sub_sub_catid, \
                    brand, \
                    is_official_shop, \
                    view_count, \
                    stock, \
                    category, \
                    sub_category, \
                    sub_sub_category, \
                    pagenum \
                         ) \
                VALUES( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )", \
                         ( \
                             itemid,
                             rating_star,
                             name,
                             price,
                             shopid,
                             shopee_verified,
                             sold,
                             catid,
                             sub_catid,
                             sub_sub_catid,
                             brand,
                             is_official_shop,
                             view_count,
                             stock,
                             category,
                             sub_category,
                             sub_sub_category,
                             pagenum
                         ))

        self.con.commit()

    def storeShopInfoInDb(self, item):
        username = item.get('username', '')
        rating_normal = item.get('rating_normal', '')
        followed = item.get('followed', '')
        following_count = item.get('following_count', '')
        userid = item.get('userid', '')
        is_free_shipping = item.get('is_free_shipping', '')
        shopid = item.get('shopid', '')
        rating_bad = item.get('rating_bad', '')
        preparation_time = item.get('preparation_time', '')
        portrait = item.get('portrait', '')
        is_shopee_verified = item.get('is_shopee_verified', '')
        show_low_fulfillment_warning = item.get('show_low_fulfillment_warning', '')
        item_count = item.get('item_count', '')
        show_official_shop_label = item.get('show_official_shop_label', '')
        follower_count = item.get('follower_count', '')
        enable_display_unitno = item.get('enable_display_unitno', '')
        status = item.get('status', '')
        is_blocking_owner = item.get('is_blocking_owner', '')
        description = item.get('description', '')
        rating_good = item.get('rating_good', '')
        is_semi_inactive = item.get('is_semi_inactive', '')
        shop_covers = ''
        chat_disabled = item.get('chat_disabled', '')
        response_time = item.get('response_time', '')
        ctime = item.get('ctime', '')
        response_rate = item.get('response_rate', '')
        disable_make_offer = item.get('disable_make_offer', '')
        name = item.get('name', '')
        cover = item.get('cover', '')
        total_avg_star = item.get('total_avg_star', '')
        free_shipping_min_total = item.get('free_shipping_min_total', '')
        holiday_mode_on = item.get('holiday_mode_on', '')
        place = item.get('place', '')
        last_active_time = item.get('last_active_time', '')

        self.cur.execute("INSERT INTO Shop(\
        			username, \
                    rating_normal, \
                    followed, \
                    following_count, \
                    userid, \
                    is_free_shipping, \
                    shopid, \
                    rating_bad, \
                    preparation_time, \
                    portrait, \
                    is_shopee_verified, \
                    show_low_fulfillment_warning, \
                    item_count, \
                    show_official_shop_label, \
                    follower_count, \
                    enable_display_unitno, \
                    status, \
                    is_blocking_owner, \
                    description, \
                    rating_good, \
                    is_semi_inactive, \
                    shop_covers, \
                    chat_disabled, \
                    response_time, \
                    ctime, \
                    response_rate, \
                    disable_make_offer, \
                    name, \
                    cover, \
                    total_avg_star, \
                    free_shipping_min_total, \
                    holiday_mode_on, \
                    place, \
                    last_active_time \
        			) \
        		VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                         (
                             username,
                             rating_normal,
                             followed,
                             following_count,
                             userid,
                             is_free_shipping,
                             shopid,
                             rating_bad,
                             preparation_time,
                             portrait,
                             is_shopee_verified,
                             show_low_fulfillment_warning,
                             item_count,
                             show_official_shop_label,
                             follower_count,
                             enable_display_unitno,
                             status,
                             is_blocking_owner,
                             description,
                             rating_good,
                             is_semi_inactive,
                             shop_covers,
                             chat_disabled,
                             response_time,
                             ctime,
                             response_rate,
                             disable_make_offer,
                             name,
                             cover,
                             total_avg_star,
                             free_shipping_min_total,
                             holiday_mode_on,
                             place,
                             last_active_time
                         ))
        self.con.commit()

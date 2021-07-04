# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyPoiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    user_name = scrapy.Field()
    danmuk = scrapy.Field()
    danmuk_display_time = scrapy.Field()
    font_color = scrapy.Field()

    created_time=scrapy.Field()
    created_time_ts=scrapy.Field()
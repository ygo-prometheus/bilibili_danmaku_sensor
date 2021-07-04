# -*- coding: utf-8 -*-
# @Time    : 2021/6/22 4:46 下午
# @Author  : lichengyu
# @File    : VideoToDanmuk.py
import json
import zlib

import scrapy

from ..items import ScrapyPoiItem
from ..utils.crawl import Spider
from ..utils.spider_utils import CustomSettings
from lxml import etree


class VideoToDanmuk(Spider):
    name = 'bilibili_spider'
    allowed_domains = ['www.bilibili.com']

    c = CustomSettings()
    c.EnFakeUserAgent = True

    c.CUS_LOG_LEVEL = 'DEBUG'
    c.CUS_CONCURRENT_REQUESTS = 64
    c.CUS_DOWNLOAD_TIMEOUT = 15
    c.CUS_COOKIES_ENABLED = True
    c.CUS_CONCURRENT_REQUESTS_PER_DOMAIN = 32
    c.CUS_CONCURRENT_REQUESTS_PER_IP = 8
    c.CUS_RETRY_TIMES = 10
    c.CUS_RETRY_ENABLED = True
    c.CUS_RETRY_HTTP_CODES = list(range(301, 600))

    custom_settings = c()

    def start_requests(self):
        url = 'https://api.bilibili.com/x/v1/dm/list.so?oid=356403599'

        yield scrapy.Request(
            url=url,
            method='GET',
            callback=self.parse
        )

    def parse(self, response, **kwargs):
        try:
            data = response.text
            selector = etree.HTML(data.encode('utf-8'))
            content = selector.xpath('//d')
            for i in content:
                user = i.xpath('./@p')
                danmuk = i.xpath('./text()')
                user_message = {
                    'user_name': zlib.crc32(bytes(user[0].split(",")[6], encoding="utf-8")),
                    'danmuk': danmuk[0],
                    'danmuk_display_time': user[0].split(",")[0],
                    'font_color': user[0].split(",")[3]
                }
                yield ScrapyPoiItem(**user_message)
        except Exception:
            self.logger.error(f'sth error happend with {response.url}-----{self.ShortCut.format_exc()}')
            yield response.retry()
            return

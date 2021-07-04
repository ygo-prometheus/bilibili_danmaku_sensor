# -*- coding: utf-8 -*-
# @Time    : 2021/6/28 8:51 下午
# @Author  : lichengyu
# @File    : UpToVideo.py

import scrapy

from ..utils.crawl import Spider
from ..utils.spider_utils import CustomSettings


class VideoToDanmuk(Spider):
    name = 'up_spider'
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
        url = 'https://api.bilibili.com/x/space/arc/search?mid=2200736&ps=30&tid=0&pn=1&keyword=&order=pubdate&jsonp=jsonp'

        yield scrapy.Request(
            url=url,
            method='GET',
            callback=self.parse
        )

    def parse(self, response, **kwargs):
        try:
            data = response.json()
            for i in data["data"]["list"]["vlist"]:
                print("视频号："+str(i["bvid"]))
        except Exception:
            self.logger.error(f'sth error happend with {response.url}-----{self.ShortCut.format_exc()}')
            yield response.retry()
            return

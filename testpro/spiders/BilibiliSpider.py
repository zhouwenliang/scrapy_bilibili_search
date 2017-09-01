# -*- coding: utf-8 -*-
# This Python file uses the following encoding: utf-8
import urllib

import re
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.spiders import Rule

from testpro.items import BilibiliItem
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class BilibiliSpider(scrapy.Spider):
    name = "bilibili"
    allowed_domains = ["bilibili.com"]
    page = 1
    url_prefix = "http://search.bilibili.com/all?keyword=" + urllib.quote("新垣结衣") + "&page="
    start_urls = [
        url_prefix + str(page)
    ]
    rules = (
        # 将所有符合正则表达式的url加入到抓取列表中
        Rule(LinkExtractor(allow=(r'http://search.bilibili.com/all?keyword=\w+&page=\d+'))),
    )

    def parse(self, response):
        # print response.body.encode("gbk", 'ignore')
        # data = response.body.encode("gbk", 'ignore')
        for item in response.xpath('//li[@class="video matrix "]').extract():
            bilibiliItem = BilibiliItem()
            selector = Selector(text=item)
            bilibiliItem['title'] = str(selector.xpath('//a[@lnk-type="video"]/@title').extract_first()).decode("utf-8")
            bilibiliItem['url'] = str(selector.xpath('//a[@lnk-type="video"]/@href').extract_first())[2:]
            bilibiliItem['img'] = str(selector.xpath('//img/@data-src').extract_first())[2:]
            bilibiliItem['time'] = str(selector.xpath('//span[@class="so-icon time"]').extract_first())
            pattern = re.compile("[0-9]{4}\-[0-9]{2}\-[0-9]{2}")
            match = pattern.search(bilibiliItem['time'])
            if match:
                # 使用Match获得分组信息
                bilibiliItem['time'] = match.group()

            bilibiliItem['desc'] = str(selector.xpath('//div[@class="des hide"]/text()').extract_first()).strip()
            yield bilibiliItem

        if len(response.xpath('//*[@id="video-paging"]/a[@class="nextPage"]')) > 0 :
            self.page = self.page + 1
            yield scrapy.Request(self.url_prefix + str(self.page))
        # if self.page < 50:
        #     self.page = self.page + 1
        #     print "paging = ", self.url_prefix + str(self.page)
        #     yield scrapy.Request(self.url_prefix + str(self.page))

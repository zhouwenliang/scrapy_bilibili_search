# -*- coding: utf-8 -*-
import scrapy
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

class BilibiliItem(scrapy.Item):
    title = scrapy.Field()
    img = scrapy.Field()
    time = scrapy.Field()
    desc = scrapy.Field()
    url = scrapy.Field()
    local_pic = scrapy.Field()

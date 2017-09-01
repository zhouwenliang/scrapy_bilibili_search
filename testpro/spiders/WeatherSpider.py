# -*- coding: utf-8 -*-
# This Python file uses the following encoding: utf-8
import scrapy
from scrapy.selector import Selector
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class WeatherSpider(scrapy.Spider):
    name = "weather"
    allowed_domains = ["http://guangzhou.tianqi.com"]
    start_urls = [
        "http://guangzhou.tianqi.com"
    ]

    def parse(self, response):
        print "response.body = ", response.body
        for temp in response.xpath('//span[@id="t_temp"]/font[1]/text()').extract():
            print "h_temp", temp
        for temp in response.xpath('//span[@id="t_temp"]/font[2]/text()').extract():
            print "l_temp", temp
        for weather in response.xpath('//li[@class="cDRed"]/text()').extract():
            weather = weather
            print "weather", weather
        for wind in response.xpath('//div[@id="today"]/ul/li[@style="height:18px;overflow:hidden"]/text()').extract():
            wind = wind
            print "wind", wind
        for cur_temp in response.xpath('//div[@id="rettemp"]/strong/text()').extract():
            cur_temp = cur_temp[0:-1]
            print "cur_temp", cur_temp.encode("utf-8")[0:-1]

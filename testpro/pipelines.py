# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json

import scrapy
import settings
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class TestproPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonPipeline(object):
    def __init__(self):
        self.file = codecs.open('D://bilibili.json', 'wb', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line.decode("unicode_escape"))
        return item



class FilterPipeline(object):
    def process_item(self, item, spider):
        year = int(item['time'][0:4])
        if (year > 2015):
            return item
        else:
            raise DropItem("year before 2016")


class ImgPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        yield scrapy.Request("http://" + item['img'])

    def item_completed(self, results, item, info):
        #获取下载地址
        print type(results) ,
        print "results = ", results
        image_path = None
        if (results[0][0]):
            image_path = results[0][1]['path']

        #判断是否成功
        if not image_path:
            raise DropItem("Item contains no images")
        #将地址存入item
        item['local_pic'] = settings.IMAGES_STORE + '/' + image_path
        return item
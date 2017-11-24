# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class ZlPipeline(object):
    # def open_spider(self, spider):
    #     self.file = open('zhil.json', 'w')
    #
    #     pass
    def __init__(self):
        self.file = open('zhilian_django.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        # 将字典转成字符串
        str_data = json.dumps(dict(item), ensure_ascii=False) + ',\n'
        # 写入文件
        self.file.write(str_data)

        return item

    def close_spider(self, spider):
        self.file.close()

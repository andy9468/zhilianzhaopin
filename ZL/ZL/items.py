# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZlItem(scrapy.Item):
    # define the fields for your item here like:
    job_name = scrapy.Field()
    job_link = scrapy.Field()
    company = scrapy.Field()
    salary = scrapy.Field()
    site = scrapy.Field()
    pub_time = scrapy.Field()
    page_num = scrapy.Field()
    line_num = scrapy.Field()
    job_content = scrapy.Field()
    site_detail = scrapy.Field()
    pass

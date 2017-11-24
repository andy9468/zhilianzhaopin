# -*- coding: utf-8 -*-
import json

import chardet
import scrapy
from ..items import ZlItem


class ZhilianSpider(scrapy.Spider):
    name = 'zhilian'
    allowed_domains = ['zhaopin.com']
    start_urls = ['http://sou.zhaopin.com/jobs/searchresult.ashx?jl=深圳&kw=python&sm=0&p=2']

    def parse(self, response):
        # 获取列表节点
        node_list = response.xpath('//td/../..')
        # print(dir(node_list))
        print(len(node_list))

        # 遍历节点
        for i, node in enumerate(node_list):
            # temp = {}
            temp = ZlItem()
            temp['job_name'] = node.xpath('./tr[1]/td[1]/div/a').xpath('string(.)').extract()[0]
            temp['job_link'] = node.xpath('./tr[1]/td[1]/div/a/@href').extract()[0]
            temp['company'] = node.xpath('./tr/td[@class="gsmc"]/a[1]/text()').extract_first()
            temp['salary'] = node.xpath('./tr/td[@class="zwyx"]/text()').extract()[0]
            temp['site'] = node.xpath('./tr/td[@class="gzdd"]/text()').extract()[0]
            temp['pub_time'] = node.xpath('./tr/td[@class="gxsj"]/span/text()').extract_first()
            temp['page_num'] = int(node.xpath('//ul/li/a[@class="current"]/text()').extract_first())
            temp['line_num'] = i + 1
            # yield temp
            yield scrapy.Request(temp['job_link'], callback=self.parse_detail, meta={"meta_1": temp})
        # 获取下一页
        try:
            next_url = response.xpath('//li[@class="pagesDown-pos"]/a/@href').extract()[0]
            yield scrapy.Request(next_url, callback=self.parse)
        except Exception as e:
            print(e)
        pass

    def parse_detail(self, response):
        item = response.meta['meta_1']
        # print('=======',type(item))

        try:
            node = response.xpath('//div[@class="tab-inner-cont"]/b/..')
            page_detail = ''.join(node.xpath('string(.)').extract()[0].split()).split('工作地址：')
            item['job_content'] = page_detail[0]
            item['site_detail'] = page_detail[1].replace('查看职位地图', '')
        except Exception as e:
            print(e)
            print('222++++++++', item['page_num'], '页', item['line_num'], '行', item['job_link'])
            try:
                page_detail = response.xpath('//div[@class="cJob_Detail f14"]/p').xpath('string(.)')  # .extract()[0]
                if page_detail is not None:
                    page_detail = page_detail.extract()

                item['job_content'] = page_detail[0]
                item['site_detail'] = None
            except Exception as e:
                print(e)
                print("333========", item['page_num'], '页', item['line_num'], '行', item['job_link'])
                try:
                    page_detail = response.xpath(
                        '//div[@class="terminalpage-main clearfix"]/div[@class="tab-cont-box"]/div[1]').xpath(
                        'string(.)')  # .extract()[0]
                    if page_detail is not None:
                        page_detail = page_detail.extract()

                    item['job_content'] = page_detail[0].strip()
                    item['site_detail'] = None
                except Exception as e:
                    print(e)
                    print("444========", item['page_num'], '页', item['line_num'], '行', item['job_link'])

        # print(item['page_num'],'页',item['line_num'],'行--------', page_detail)
        yield item

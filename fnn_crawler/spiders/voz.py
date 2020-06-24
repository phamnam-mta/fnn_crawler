from datetime import datetime
import hashlib
import os
import re

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join
from fnn_crawler.items import VozItem

class VozSpider(scrapy.Spider):
    name = 'voz'
    allowed_domains = ['voz.vn']
    start_urls = [
        'https://voz.vn/f/chuyen-tro-linh-tinh.17/'
    ]

    def parse(self, response):

        thread_name = response.xpath('//h1[@class="p-title-value"]/text()').get()
        if thread_name:
            hashcode = hashlib.md5(thread_name.encode('utf-8')).hexdigest()

            for reply in response.xpath('//div[@class="message-inner"]'):
                l = ItemLoader(item = VozItem(),selector=reply)
                l.add_value('thread', thread_name)
                l.add_value('hashcode', hashcode)
                l.add_xpath('user', './/h4[@class="message-name"]/a/text()')
                l.add_xpath('quote', './/div[@class="bbCodeBlock-expandContent "]')
                l.add_xpath('reply', './/div[@class="bbWrapper"]/text()')
                l.add_xpath('ordinal_numbers', './/ul', re=r'#\d+')
                l.add_xpath('post_time', './/time/@datetime')
                l.add_value('scrape_time', str(datetime.now()))

                yield l.load_item()

        if os.stat("voz_informal_text.json").st_size/1000000 < 5000:
            for href in response.xpath('//a/@href').getall():
                if re.search(r'/f/|/t/', href) and re.search(r'post-\d+', href) == None:
                    yield scrapy.Request(response.urljoin(href), self.parse)
                

            
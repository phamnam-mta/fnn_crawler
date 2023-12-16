from datetime import datetime
import hashlib
import os
import re
import psutil

import scrapy
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags
from fnn_crawler.items import VozItem
from scrapy.exceptions import CloseSpider

class VozSpider(scrapy.Spider):
    name = 'voz'
    allowed_domains = ['voz.vn']
    start_urls = [
            'https://voz.vn/f/chuyen-tro-linh-tinh.17/',
            'https://voz.vn/f/diem-bao.33/',
            'https://voz.vn/f/from-f17-with-love.69/',
            'https://voz.vn/f/truyen-voz.96/',
            'https://voz.vn/f/the-duc-the-thao.63/',
            'https://voz.vn/f/thoi-trang-lam-dep.66/',
            'https://voz.vn/',
    ]

    def parse(self, response):
        for href in response.xpath('//a/@href').getall():
            page_number = re.search(r'/page-\d+', href)
            if "/t/" in href and page_number:
                if int(re.search(r'\d+', page_number.group()).group()) <= 25:
                    yield scrapy.Request(response.urljoin(href), self.parse)
            elif re.search(r'/f/|/t/', href) and re.search(r'post-\d+', href) == None and re.search(r'/latest', href) == None:
                yield scrapy.Request(response.urljoin(href), self.parse)

        thread_name = response.xpath('//h1[@class="p-title-value"]/text()').get()
        replies = response.xpath('//div[@class="message-inner"]')
        if thread_name and len(replies) >= 5:
            hashcode = hashlib.md5(thread_name.encode('utf-8')).hexdigest()
            topic = response.xpath("//ul[@class='p-breadcrumbs ']/li/a/span/text()").getall()[1]
            sub_topic = response.xpath("//ul[@class='p-breadcrumbs ']/li/a/span/text()").getall()[2]
            for reply in replies:
                l = ItemLoader(item = VozItem(), selector=reply)
                l.add_value('thread', thread_name)
                l.add_value('hashcode', hashcode)
                l.add_value('topic', topic)
                l.add_value('source_url', response.request.url)
                l.add_value('sub_topic', sub_topic)
                l.add_xpath('user', './/h4[@class="message-name"]/a/text()')
                l.add_css('quote', '.bbCodeBlock-expandContent ::text')
                l.add_xpath('reply', './/div[@class="bbWrapper"]/text()')
                l.add_xpath('ordinal_numbers', './/ul', re=r'#\d+')
                l.add_xpath('post_time', './/time/@datetime')
                l.add_value('scrape_time', str(datetime.now()))

                yield l.load_item()
        
        if psutil.virtual_memory().percent > 90:
            raise CloseSpider("out of memory")         

            
from datetime import datetime
import hashlib
import os
import re
import psutil

import scrapy
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags
from fnn_crawler.items import OtoFunItem
from scrapy.exceptions import CloseSpider


HEADERS = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0'}

class OtoFunSpider(scrapy.Spider):
    name = 'otofun'
    allowed_domains = ['otofun.net']
    start_urls = [
            'https://www.otofun.net/forums/',
        ]
    def start_requests(self):
            for url in self.start_urls:
                yield scrapy.Request(url, headers=HEADERS)
    def parse(self, response):
        for href in response.xpath('//a/@href').getall():
            page_number = re.search(r'/page-\d+', href)
            if "/threads/" in href and page_number:
                if int(re.search(r'\d+', page_number.group()).group()) <= 30:
                    yield scrapy.Request(response.urljoin(href), self.parse, headers=HEADERS)
            elif re.search(r'/forums/|/threads/', href) and re.search(r'post-\d+', href) == None and re.search(r'/latest', href) == None:
                yield scrapy.Request(response.urljoin(href), self.parse, headers=HEADERS)

        thread_name = response.xpath('//h1[@class="p-title-value"]/text()').get()
        replies = response.xpath('//div[@class="message-inner"]')
        if thread_name and len(replies) >= 3:
            topic = response.xpath("//ul[@class='p-breadcrumbs ']/li/a/span/text()").getall()
            for reply in replies:
                l = ItemLoader(item = OtoFunItem(), selector=reply)
                l.add_value('thread', thread_name)
                l.add_value('topic', topic)
                l.add_value('source_url', response.request.url)
                l.add_xpath('user', './/h4[@class="message-name"]/a/text()')
                l.add_css('quote', '.bbCodeBlock-expandContent ::text')
                l.add_xpath('reply', './/div[@class="bbWrapper"]/text()')
                l.add_xpath('ordinal_numbers', './/ul', re=r'#\d+')
                l.add_value('scrape_time', str(datetime.now()))

                yield l.load_item()
        
        if psutil.virtual_memory().percent > 90:
            raise CloseSpider("out of memory")         

            
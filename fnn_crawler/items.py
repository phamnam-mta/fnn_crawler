# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, Join, MapCompose
from w3lib.html import remove_tags


class VozItem(scrapy.Item):
    """Voz item structure:
    {
    	'thread': 'thread name',
        'hashcode': 'hashcode of thread',
    	'user': 'user name',
    	'quote': ['text'], //if none: reply for thread, else: reply for quote
    	'reply': ['text'],
        'ordinal_numbers':'#number',
        'post_time': 'datetime'
    	'scrape_time': 'datetime',
    }
    """
    
    thread = scrapy.Field(output_processor=TakeFirst())
    hashcode = scrapy.Field(output_processor=TakeFirst())
    user = scrapy.Field(output_processor=TakeFirst())
    quote = scrapy.Field(input_processor=MapCompose(remove_tags))
    reply = scrapy.Field()
    ordinal_numbers = scrapy.Field(output_processor=TakeFirst())
    post_time = scrapy.Field(output_processor=TakeFirst())
    scrape_time = scrapy.Field(output_processor=TakeFirst())
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, Join, MapCompose


class VozItem(scrapy.Item):
    """Voz item structure:
    {
    	'thread': 'thread name',
        'hashcode': 'hashcode of thread',
    	'user': 'user name',
        'topic': 'topic',
        'source_url': 'source',
        'sub_topic': 'sub_topic',
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
    topic = scrapy.Field(output_processor=TakeFirst())
    sub_topic = scrapy.Field(output_processor=TakeFirst())
    source_url = scrapy.Field(output_processor=TakeFirst())
    quote = scrapy.Field()
    reply = scrapy.Field()
    ordinal_numbers = scrapy.Field(output_processor=TakeFirst())
    post_time = scrapy.Field(output_processor=TakeFirst())
    scrape_time = scrapy.Field(output_processor=TakeFirst())

class OtoFunItem(scrapy.Item):
    """OtoFun item structure:
    {
    	'thread': 'thread name',
    	'user': 'user name',
        'topic': 'topic',
        'source_url': 'source',
    	'quote': ['text'], //if none: reply for thread, else: reply for quote
    	'reply': ['text'],
        'ordinal_numbers':'#number',
    	'scrape_time': 'datetime',
    }
    """
    
    thread = scrapy.Field(output_processor=TakeFirst())
    user = scrapy.Field(output_processor=TakeFirst())
    topic = scrapy.Field(output_processor=TakeFirst())
    source_url = scrapy.Field(output_processor=TakeFirst())
    quote = scrapy.Field()
    reply = scrapy.Field()
    ordinal_numbers = scrapy.Field(output_processor=TakeFirst())
    scrape_time = scrapy.Field(output_processor=TakeFirst())
class TinhTeThreadItem(scrapy.Item):
    """Tinhte thread item structure:
    {
        "thread_id": 3419123,
        "forum_id": 10,
        "thread_title": "Bạn còn giữ những món đồ công nghệ huyền thoại nào không?",
        "thread_view_count": 6421,
        "creator_user_id": 2438731,
        "creator_username": "myhien.bui",
        "thread_create_date": 1634358101,
        "thread_update_date": 1634626484,
        "thread_post_count": 130,
        'topic': 'topic',
        'sub_topic': 'sub_topic',
        'source_url': 'source',
        "first_post": {
            "post_id": 61171903,
            "thread_id": 3419123,
            "poster_user_id": 2438731,
            "poster_username": "myhien.bui",
            "post_create_date": 1634353637,
            "post_body_plain_text": "",
            "post_like_count": 3,
            "like_users": [],
            "post_update_date": 1634470125,
            "poster_rank": {
                "rank_level": 3,
                "rank_name": "CAO CẤP",
                "rank_group_id": 59,
                "rank_points": 35386
            }
        },
    	'scrape_time': 'datetime',
    }
    """
    thread_id = scrapy.Field(output_processor=TakeFirst())
    forum_id = scrapy.Field(output_processor=TakeFirst())
    thread_title = scrapy.Field(output_processor=TakeFirst())
    thread_view_count = scrapy.Field(output_processor=TakeFirst())
    creator_user_id = scrapy.Field(output_processor=TakeFirst())
    creator_username = scrapy.Field(output_processor=TakeFirst())
    thread_create_date = scrapy.Field(output_processor=TakeFirst())
    thread_update_date = scrapy.Field(output_processor=TakeFirst())
    thread_post_count = scrapy.Field(output_processor=TakeFirst())
    topic = scrapy.Field(output_processor=TakeFirst())
    sub_topic = scrapy.Field(output_processor=TakeFirst())
    source_url = scrapy.Field(output_processor=TakeFirst())
    first_post = scrapy.Field(output_processor=TakeFirst())
    scrape_time = scrapy.Field(output_processor=TakeFirst())

class TinhTePostItem(scrapy.Item):
    """Tinhte post item structure:
    {
        "post_id": 61172559,
        "thread_id": 3419123,
        "poster_user_id": 210010,
        "poster_username": "crazysexycool1981",
        "post_create_date": 1634359044,
        "post_body_plain_text": "",
        "post_like_count": 5,
        "like_users": [],
        "post_update_date": 1634359437,,
        "poster_rank": {
            "rank_level": 4,
            "rank_name": "VIP",
            "rank_group_id": 60,
            "rank_points": 2486670.19
        },
        "post_replies": [],
        "replies": [
            #post item
        ]
        'source_url': 'source',
    	'scrape_time': 'datetime',
    }
    """
    post_id = scrapy.Field(output_processor=TakeFirst())
    thread_id = scrapy.Field(output_processor=TakeFirst())
    poster_user_id = scrapy.Field(output_processor=TakeFirst())
    poster_username = scrapy.Field(output_processor=TakeFirst())
    post_create_date = scrapy.Field(output_processor=TakeFirst())
    post_body_plain_text = scrapy.Field(output_processor=TakeFirst())
    post_like_count = scrapy.Field(output_processor=TakeFirst())
    like_users = scrapy.Field(output_processor=TakeFirst())
    post_update_date = scrapy.Field(output_processor=TakeFirst())
    poster_rank = scrapy.Field(output_processor=TakeFirst())
    post_replies = scrapy.Field()
    replies = scrapy.Field()
    source_url = scrapy.Field(output_processor=TakeFirst())
    scrape_time = scrapy.Field(output_processor=TakeFirst())
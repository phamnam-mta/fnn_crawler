from datetime import datetime
import hashlib
import os
import re
import requests
import json
import psutil

import scrapy
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags
from fnn_crawler.items import TinhTePostItem, TinhTeThreadItem
from scrapy.exceptions import CloseSpider

class TinhTeSpider(scrapy.Spider):
    name = 'tinhte'
    allowed_domains = ['tinhte.vn', 'camera.tinhte.vn', 'xe.tinhte.vn']
    start_urls = [
            'https://tinhte.vn/forums/',
            'https://xe.tinhte.vn/',
            'https://camera.tinhte.vn/',
            'https://tinhte.vn/forums/thong-tin-cong-nghe.10/',
            'https://tinhte.vn/forums/dam-may-dich-vu-truc-tuyen.460/',
            'https://tinhte.vn/forums/nhiem-vu-tinh-te.745/',
            'https://tinhte.vn/categories/he-dieu-hanh-windows.6/',
            'https://tinhte.vn/forums/may-tinh-mac-macos.748/',
            'https://tinhte.vn/forums/tu-van-chon-mua-may-tinh.199/',
            'https://tinhte.vn/forums/thiet-bi-mang.759/',
            'https://tinhte.vn/forums/iphone-ipad-ios.746/',
            'https://tinhte.vn/forums/android.747/',
            'https://tinhte.vn/categories/blackberry.98/',
            'https://tinhte.vn/categories/symbian.83/',
            'https://tinhte.vn/forums/xe-may.544/',
            'https://tinhte.vn/forums/khoa-hoc.76/',
            'https://tinhte.vn/forums/xe-o-to.545/',
            'https://tinhte.vn/forums/ca-phe-tinh-te.36/'
        ]

    def parse(self, response):
        for href in response.xpath('//a/@href').getall():
            if re.search(r'thread|forums|categories', href) and re.search(r'post-\d+', href) == None and re.search(r'/thread/page-\d+', href) == None:
                yield scrapy.Request(response.urljoin(href), self.parse)

        is_thread = re.search(r'/thread/', response.request.url)
        if is_thread:
            page_number = re.search(r'/page-\d+', response.request.url)
            content = response.xpath('//script[re:test(text(),"oauth_token=","i")]').get()
            oauth_token = re.search('oauth_token=(.+?)zolu', content).group().split("oauth_token=")[1]
            if page_number:
                # crawl post
                post_ids = response.xpath("//div[@class='jsx-726421895 thread-comment__box   ']/@id").getall()
                print("---------------", post_ids)
                print("---------------", response.request.url)
                for id in post_ids:
                    post_id = id.split('-')[1]
                    api_url = f"https://tinhte.vn/appforo/index.php?posts/{post_id}/replies&oauth_token={oauth_token}"
                    print("----------Post---------", api_url)
                    resp = requests.get(api_url)
                    if resp.status_code == 200:
                        data = resp.json()
                        l = ItemLoader(item = TinhTePostItem())
                        l.add_value('post_id', data["parent_post"].get("post_id"))
                        l.add_value('thread_id', data["parent_post"].get("thread_id"))
                        l.add_value('poster_user_id', data["parent_post"].get("poster_user_id"))
                        l.add_value('poster_username', data["parent_post"].get("poster_username"))
                        l.add_value('post_create_date', data["parent_post"].get("post_create_date"))
                        l.add_value('post_body_plain_text', data["parent_post"].get("post_body_plain_text"))
                        l.add_value('post_like_count', data["parent_post"].get("post_like_count"))
                        l.add_value('like_users', data["parent_post"].get("like_users"))
                        l.add_value('post_update_date', data["parent_post"].get("post_update_date"))
                        l.add_value('poster_rank', data["parent_post"].get("poster_rank"))
                        l.add_value('post_replies', data["parent_post"].get("post_replies"))
                        l.add_value('source_url', data["parent_post"]["links"].get("permalink"))
                        l.add_value('scrape_time', str(datetime.now()))

                        replies = []
                        for r in data["replies"]:
                            quote = re.search('\[QUOTE=(.+?)\]', r.get("post_body"))
                            replies.append({
                                "post_id": r.get("post_id"),
                                "thread_id": r.get("thread_id"),
                                "poster_user_id": r.get("poster_user_id"),
                                "poster_username": r.get("poster_username"),
                                "post_create_date": r.get("post_create_date"),
                                "quote": quote.group() if quote else "",
                                "post_body_plain_text": r.get("post_body_plain_text"),
                                "post_like_count": r.get("post_like_count"),
                                "like_users": r.get("like_users"),
                                "post_update_date": r.get("post_update_date"),
                                "poster_rank": r.get("poster_rank"),
                            })
                        l.add_value('replies', replies)
                        yield l.load_item()
            else:
                raw_thread_id = re.search(r'\.\d+/$', response.request.url)
                thread_id = re.search(r'\d+', raw_thread_id.group()).group()
                
                # crawl thread
                api_url = f"https://tinhte.vn/appforo/index.php?threads/{thread_id}&oauth_token={oauth_token}"
                print("---------Thread----------", api_url)
                resp = requests.get(api_url)
                if resp.status_code == 200:
                    data = resp.json()
                    thread = data["thread"]
                    l = ItemLoader(item = TinhTeThreadItem())
                    l.add_value('thread_id', thread_id)
                    l.add_value('forum_id', thread["forum_id"])
                    l.add_value('thread_title', thread["thread_title"])
                    l.add_value('thread_view_count', thread["thread_view_count"])
                    l.add_value('creator_user_id', thread["creator_user_id"])
                    l.add_value('creator_username', thread["creator_username"])
                    l.add_value('thread_create_date', thread["thread_create_date"])
                    l.add_value('thread_update_date', thread["thread_update_date"])
                    l.add_value('thread_post_count', thread["thread_post_count"])

                    first_post= {
                        "post_id": thread["first_post"].get("post_id"),
                        "thread_id": thread["first_post"].get("thread_id"),
                        "poster_user_id": thread["first_post"].get("poster_user_id"),
                        "poster_username": thread["first_post"].get("poster_username"),
                        "post_create_date": thread["first_post"].get("post_create_date"),
                        "post_body_plain_text": thread["first_post"].get("post_body_plain_text"),
                        "post_like_count": thread["first_post"].get("post_like_count"),
                        "like_users": thread["first_post"].get("like_users"),
                        "post_update_date": thread["first_post"].get("post_update_date"),
                        "poster_rank": thread["first_post"].get("poster_rank"),
                    }
                    l.add_value('first_post', first_post)

                    topic = response.xpath("//a[@class='jsx-3147581474 label']/text()").getall()
                    l.add_value('topic', topic[0])
                    l.add_value('sub_topic', topic[1])
                    l.add_value('source_url', response.request.url)
                    l.add_value('scrape_time', str(datetime.now()))

                    yield l.load_item()

                # crawl post
                post_ids = response.xpath("//div[@class='jsx-726421895 thread-comment__box   ']/@id").getall()
                print("---------------", post_ids)
                print("---------------", response.request.url)
                for id in post_ids:
                    post_id = id.split('-')[1]
                    api_url = f"https://tinhte.vn/appforo/index.php?posts/{post_id}/replies&oauth_token={oauth_token}"
                    print("----------Post---------", api_url)
                    resp = requests.get(api_url)
                    if resp.status_code == 200:
                        data = resp.json()
                        l = ItemLoader(item = TinhTePostItem())
                        l.add_value('post_id', data["parent_post"].get("post_id"))
                        l.add_value('thread_id', data["parent_post"].get("thread_id"))
                        l.add_value('poster_user_id', data["parent_post"].get("poster_user_id"))
                        l.add_value('poster_username', data["parent_post"].get("poster_username"))
                        l.add_value('post_create_date', data["parent_post"].get("post_create_date"))
                        l.add_value('post_body_plain_text', data["parent_post"].get("post_body_plain_text"))
                        l.add_value('post_like_count', data["parent_post"].get("post_like_count"))
                        l.add_value('like_users', data["parent_post"].get("like_users"))
                        l.add_value('post_update_date', data["parent_post"].get("post_update_date"))
                        l.add_value('poster_rank', data["parent_post"].get("poster_rank"))
                        l.add_value('post_replies', data["parent_post"].get("post_replies"))
                        l.add_value('source_url', data["parent_post"]["links"].get("permalink"))
                        l.add_value('scrape_time', str(datetime.now()))

                        replies = []
                        for r in data["replies"]:
                            quote = re.search('\[QUOTE=(.+?)\]', r.get("post_body"))
                            replies.append({
                                "post_id": r.get("post_id"),
                                "thread_id": r.get("thread_id"),
                                "poster_user_id": r.get("poster_user_id"),
                                "poster_username": r.get("poster_username"),
                                "post_create_date": r.get("post_create_date"),
                                "quote": quote.group() if quote else "",
                                "post_body_plain_text": r.get("post_body_plain_text"),
                                "post_like_count": r.get("post_like_count"),
                                "like_users": r.get("like_users"),
                                "post_update_date": r.get("post_update_date"),
                                "poster_rank": r.get("poster_rank"),
                            })
                        l.add_value('replies', replies)
                        yield l.load_item()
            
            # extract thread page
            pages = response.xpath("//a[@class='jsx-2305813501 page ']/@href").getall()
            for p in pages:
                page_number = re.search(r'/page-\d+', p)
                if page_number and int(re.search(r'\d+', page_number.group()).group()) <= 20:
                    if re.search(r'/page-\d+', response.request.url):
                        page_url = re.sub(r'/page-\d+', page_number.group(), response.request.url)
                    else:
                        page_url = response.request.url + page_number.group()
                    print("page_url", page_url)
                    yield scrapy.Request(page_url, self.parse)

        if psutil.virtual_memory().percent > 90:
            raise CloseSpider("out of memory")        

            
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
from scrapy.exporters import JsonItemExporter
from fnn_crawler.items import TinhTePostItem, TinhTeThreadItem

# class FnnCrawlerPipeline:
#     def process_item(self, item, spider):
#         return item

class JsonVozPipeline(object):
    def __init__(self):
        self.file_number = 1
        self.file_name = "voz_corpus"
        self.file_path = f'fnn_crawler/data/voz/{self.file_name}_{self.file_number}.json'
        self.file = open(self.file_path, 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def open_new_file(self):
        self.exporter.finish_exporting()
        self.file.close()
        self.file_number += 1
        self.file_path = f'fnn_crawler/data/voz/{self.file_name}_{self.file_number}.json'

        self.file = open(self.file_path, 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        if os.stat(self.file_path).st_size/1000000 < 100: # file size must < 100Mb
            self.exporter.export_item(item)
        else:
            self.open_new_file()
            self.exporter.export_item(item)
        return item

class OtoFunPipeline(object):
    def __init__(self):
        self.file_number = 1
        self.file_name = "otofun_corpus"
        self.file_path = f'fnn_crawler/data/otofun/{self.file_name}_{self.file_number}.json'
        self.file = open(self.file_path, 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def open_new_file(self):
        self.exporter.finish_exporting()
        self.file.close()
        self.file_number += 1
        self.file_path = f'fnn_crawler/data/otofun/{self.file_name}_{self.file_number}.json'

        self.file = open(self.file_path, 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        if os.stat(self.file_path).st_size/1000000 < 100: # file size must < 100Mb
            self.exporter.export_item(item)
        else:
            self.open_new_file()
            self.exporter.export_item(item)
        return item

class JsonTinhTePipeline(object):
    def __init__(self):
        # Thread
        self.file_number_thread = 1
        self.file_name_thread = "tinhte_corpus_thread"
        self.file_path_thread = f'fnn_crawler/data/tinhte/{self.file_name_thread}_{self.file_number_thread}.json'
        self.file_thread = open(self.file_path_thread, 'wb')
        self.exporter_thread = JsonItemExporter(self.file_thread, encoding='utf-8', ensure_ascii=False)
        self.exporter_thread.start_exporting()

        # Post
        self.file_number_post = 1
        self.file_name_post = "tinhte_corpus_post"
        self.file_path_post = f'fnn_crawler/data/tinhte/{self.file_name_post}_{self.file_number_post}.json'
        self.file_post = open(self.file_path_post, 'wb')
        self.exporter_post = JsonItemExporter(self.file_post, encoding='utf-8', ensure_ascii=False)
        self.exporter_post.start_exporting()

    def open_new_file_thread(self):
        self.exporter_thread.finish_exporting()
        self.file_thread.close()
        self.file_number_thread += 1
        self.file_path_thread = f'fnn_crawler/data/tinhte/{self.file_name_thread}_{self.file_number_thread}.json'

        self.file_thread = open(self.file_path_thread, 'wb')
        self.exporter_thread = JsonItemExporter(self.file_thread, encoding='utf-8', ensure_ascii=False)
        self.exporter_thread.start_exporting()

    def open_new_file_post(self):
        self.exporter_post.finish_exporting()
        self.file_post.close()
        self.file_number_post += 1
        self.file_path_post = f'fnn_crawler/data/tinhte/{self.file_name_post}_{self.file_number_post}.json'

        self.file_post = open(self.file_path_post, 'wb')
        self.exporter_post = JsonItemExporter(self.file_post, encoding='utf-8', ensure_ascii=False)
        self.exporter_post.start_exporting()

    def close_spider(self, spider):
        self.exporter_thread.finish_exporting()
        self.file_thread.close()
        self.exporter_post.finish_exporting()
        self.file_post.close()

    def process_item(self, item, spider):
        if isinstance(item, TinhTeThreadItem):
            if os.stat(self.file_path_thread).st_size/1000000 < 100: # file size must < 100Mb
                self.exporter_thread.export_item(item)
            else:
                self.open_new_file_thread()
                self.exporter_thread.export_item(item)
        else:
            if os.stat(self.file_path_post).st_size/1000000 < 100: # file size must < 100Mb
                self.exporter_post.export_item(item)
            else:
                self.open_new_file_post()
                self.exporter_post.export_item(item)
        return item
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from NewsSpider.db import connectDb

class NewsspiderPipeline(object):
    def process_item(self, item, spider):
        print(item['title'])
        query = 'insert into news_preview(author, fpTime, title, tags, url, content) value ("%s", "%s", "%s", "%s", "%s", "%s")' % (item['author'], item['fpTime'], item['title'], item['tags'], item['url'], item['content'])
        self.cur.execute(query)
        self.conn.commit()
        return item

    def open_spider(self, spider):
        self.conn = connectDb()
        self.cur = self.conn.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

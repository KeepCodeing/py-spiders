# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy



class NewsspiderItem(scrapy.Item):
    author = scrapy.Field()
    fpTime = scrapy.Field()
    title = scrapy.Field()
    tags = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()




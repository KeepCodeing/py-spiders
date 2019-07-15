# -*- coding: utf-8 -*-
import scrapy
import json
import datetime
from NewsSpider.items import NewsspiderItem


class XinlangSpider(scrapy.Spider):
    name = 'xinlang'
    allowed_domains = ['sina.com.cn']
    start_urls = ['https://cre.mix.sina.com.cn/api/v3/get?cre=tianyi&mod=pctech&offset=0']
    def __init__(self):
        super(XinlangSpider, self).__init__(self)
        self.page = 0

    def parse(self, response):
        ret_data = json.loads(response.text)
        for i in ret_data['data']:
            item = NewsspiderItem()
            item['author'] = i['author']
            item['fpTime'] = datetime.datetime.utcfromtimestamp(int(i['fpTime'])).strftime('%Y.%m.%d %H:%M:%S')
            item['title'] = i['title']
            item['tags'] = str({'tags':i['tags']})
            item['url'] = i['url_https']
            yield scrapy.Request(
                item['url'],
                callback=self.parse_content,
                meta={'item':item}
            )

        self.page += 1
        next_url = 'https://cre.mix.sina.com.cn/api/v3/get?cre=tianyi&mod=pctech&offset={page}'.format(page=str(self.page))
        yield scrapy.Request(
            next_url,
            callback=self.parse
        )

    def parse_content(self, response):
        content = response.xpath('//div[@id="artibody"]').get()
        item = response.meta['item']
        if content != None:
            # 将双引号换成单引号，否则sql语句无法执行
            item['content'] = content.replace('"', '\'')
            yield item

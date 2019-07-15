# -*- coding: utf-8 -*-
'''
需要爬取的东西
0. 爬取的漫画的书名（只爬取一次）
1. 章节标题（每一章只爬取一次）
2. 每页的图片
@PC YJSP
@FileName main
@Author hwz
@Date 2019/7/10 15:10
@ProjectName py-projects
'''
import scrapy
from NewComicGetter.items import NewcomicgetterItem
import re
import os


class MainSpider(scrapy.Spider):
    name = 'dn'
    allowed_domains = ['manhuadb.com']
    # 死亡笔记
    start_urls = ['https://www.manhuadb.com/manhua/144/67_740.html']

    def __init__(self):
        super(MainSpider, self).__init__(self)
        self.all_pages = []

    def parse(self, response):
        item = NewcomicgetterItem()
        # 漫画标题，可用来作为保存文件的根目录
        item['comic_title'] = response.xpath('//h1[@class="h2 text-center mt-3"]/a/text()').get()
        # 获取全部章节url
        # 通过切片来去除已经爬取过了的url
        self.all_pages = (response.xpath('//li[@class="sort_div "]/a/@href').getall())[1:]
        yield scrapy.Request(
            callback=self.parse_next_page,
            meta={'item':item},
            url='https://www.manhuadb.com' + self.all_pages.pop(0)
        )
        # 持久化数据
        self.keep_data(item['comic_title'])
        # 新建根文件夹
        self.creatRootFile(item)

    def creatRootFile(self, item):
        # 新建根文件夹
        try:
            os.mkdir('./' + item['comic_title'])
        except IOError:
            print('文件IO出错\n')

    def creatChildFile(self, item):
        # 新建章节文件夹
        os.mkdir('./' + item['comic_title'] + '/' + item['title'])

    def keep_data(self, data):
        # 本地数据持久化
        file = open('./MOSHOU.txt', 'a')
        file.writelines(data + '\n')
        file.close()

    # 用来提取章节标题，初始化图片url
    def parse_next_page(self, response):
        item = response.meta['item']
        # 章节标题,在获取新一章内容时提取
        item['title'] = response.xpath('//h2[@class="h4 text-center"]/text()').get()
        item['img_url'] = []
        self.keep_data(item['title'])
        yield scrapy.Request(
            callback=self.parse_img,
            meta={'item':item},
            url=response.url,
            # 设置不去重
            dont_filter=True
        )

    # 解析图片
    def parse_img(self, response):
        # 翻到了最后一页的a标签的url
        # javascript:alert('本章已完，前往下一章！');goNumPage('next');
        # 通过正则表达式匹配下一页url是否包含"本章已完",如果包含，则翻页爬取
        item = response.meta['item']
        next_page = response.xpath('//a[text()="下页"]/@href').get()
        if not re.findall("本章已完", next_page):
            img_url = 'https://www.manhuadb.com' + response.xpath('//img[@class="img-fluid"]/@src').get()
            print('*' * 10 + img_url + '*' * 10)
            item['img_url'].append(img_url)
            self.keep_data(img_url)
            yield scrapy.Request(
                url='https://www.manhuadb.com' + next_page,
                callback=self.parse_img,
                meta={'item':item}
            )
        else:
            if len(self.all_pages) > 0:
                # 创建子文件夹
                self.creatChildFile(item)
                # 发起下一页的请求
                yield scrapy.Request(
                    url='https://www.manhuadb.com' + self.all_pages.pop(0),
                    meta={'item':item},
                    callback=self.parse_next_page,
                )
                yield item
            # 当倒数第一章发送请求后数组长度已经为0，所以不会再有下一页请求，但同样需要把最后一页的数据下载下来
            elif (len(self.all_pages) == 0):
                self.creatChildFile(item)
                yield item
            else:
                print('爬取完毕！')
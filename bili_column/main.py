# -*- coding: utf-8 -*-
"""
@PC YJSP
@FileName main
@Author hwz
@Date 2019/11/15 14:33
@ProjectName py-projects
-------功能-------
爬取bilibili专栏
"""
import requests
import ua
import pandas as pd
from lxml import etree

class crawler(object):
    def __init__(self):
        self.s = requests.Session()
        header = {
            'User-agent' : ua.getUa()
        }
        self.s.headers = header
        self.data_dict = {
            'title': [],
            'images': [],
            'context': []
        }

    def start(self, cv_url):
        html = etree.HTML(self.s.get(url = "http://www.bilibili.com/read/cv{cv_url}".format(cv_url=cv_url)).text)
        column_head = html.xpath('//div[@class="head-container"]/div[@class="title-container"]')
        title = column_head[0].xpath('h1/text()')[0]
        # 解析文章内容
        column_body = html.xpath('//div[@class="article-holder"]//text()')
        data = ''
        head_img = ''
        # 解析banner图片
        head_img_body = str(html.xpath('//head/script[@type="application/ld+json"]/text()')[0]).splitlines()
        for i in head_img_body:
            if "images" in i:
                head_img += i.split(':', 1)[1][2:-2]
                break
        # 将文章内容合并
        for i in column_body:
            data += i.replace('—', '').replace(' ', '')
        # 解析文章图片
        images = html.xpath('//div[@class="article-holder"]//img[not(contains(@class, "cut-off-5"))]/@data-src')
        images = ['http://' + i for i in images]
        # 添加数据
        self.data_dict['title'].append(title)
        self.data_dict['images'].append(images)
        self.data_dict['context'].append(data)

    def be_csv(self, filename='temp'):
        pd.DataFrame(self.data_dict).to_csv('./'+filename+'.csv')


def main():
    c = crawler()
    c.start("3949523")
    c.start("3899764")
    c.be_csv()


if __name__ == '__main__':
    main()
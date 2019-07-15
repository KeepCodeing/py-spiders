# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests
import time
import threading


class NewcomicgetterPipeline(object):

    def process_item(self, item, spider):
        print("%s的%s爬取完毕！启动下载！" % (item['comic_title'], item['title']))
        # self.downloadFile(root_path=item['comic_title'], path=item['title'], name=str(item['img_url'].index(url)+1), url=url)
        for url in item['img_url']:
            dw = threading.Thread(target=self.downloadFile, args=(item['comic_title'], item['title'], str(item['img_url'].index(url)+1), url))
            dw.start()
            # 当下载3张图片后休眠3.5S
            if (item['img_url'].index(url)+1) % 3 == 0:
                time.sleep(3.5)
        print("%s的%s下载完毕！" % (item['comic_title'], item['title']))
        return item

    def downloadFile(self, root_path, path, name, url):
        headers = {'Proxy-Connection': 'keep-alive'}
        r = requests.get(url, stream=True, headers=headers)
        f = open('./'+root_path+'/' + path +'/' + name + '.png', 'wb')
        for chunk in r.iter_content(chunk_size=512):
            if chunk:
                f.write(chunk)
        f.close()

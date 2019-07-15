import scrapy


class NewcomicgetterItem(scrapy.Item):
    # 图片链接容器
    img_url = scrapy.Field()
    # 章节标题容器
    title = scrapy.Field()
    # 漫画标题容器
    comic_title = scrapy.Field()

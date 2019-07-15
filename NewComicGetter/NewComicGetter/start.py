"""
@PC YJSP
@FileName start
@Author hwz
@Date 2019/7/11 16:11
@ProjectName py-projects
"""
from scrapy import cmdline


def main():
    # cmdline.execute('scrapy crawl madoka'.split(' '))
    # cmdline.execute('scrapy crawl dn'.split(' '))
    # cmdline.execute('scrapy crawl mamei'.split(' '))
    # cmdline.execute('scrapy crawl moji'.split(' '))
    cmdline.execute('scrapy crawl moshou'.split(' '))

if __name__ == '__main__':
    main()
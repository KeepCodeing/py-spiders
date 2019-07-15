"""
@PC YJSP
@FileName start
@Author hwz
@Date 2019/7/4 15:59
@ProjectName py-projects
"""
from scrapy import cmdline


def main():
    try:
        cmdline.execute('scrapy crawl xinlang'.split(' '))
    except:
        print('error')


if __name__ == '__main__':
    main()

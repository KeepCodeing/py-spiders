import sys
import requests
import re
import time
import threading
from lxml import etree
import download
from random_au import random_agent


sys.setrecursionlimit(3000)


def getIp():
    html = requests.get(url='http://www.goubanjia.com/', headers=random_agent(), timeout=3)

    data = etree.HTML(html.text)

    tr = data.xpath('//tbody/tr')

    ip_list = []

    for td in tr:
        ip = ''
        isgaomi = td.xpath('td[2]/a/text()')[0]
        if isgaomi == '高匿':
            ip_temp = td.xpath('td[@class="ip"]//*[not(@style="display:none;")and(not(@style="display: none;"))and(not(not(text())))and(not(contains(@class,"port")))]/text()')
            for i in ip_temp:
                ip += i

            ip_list.append(ip)
    can_use_ip = checkIP(ip_list, ':80')
    return can_use_ip

def checkIP(ip_list, port):
    can_use_ip = []
    for ip in ip_list:
        try:
            res = requests.get(url='http://ip.tool.chinaz.com/', headers=random_agent(), proxies={'http':str(ip+port)}, timeout=3)
            if res.status_code == 200:
                html = etree.HTML(res.text)
            try:
                ret_ip = html.xpath('//dl[@class="IpMRig-tit"]/dd[@class="fz24"]//text()')[0]
                ret_pos = html.xpath('//dl[@class="IpMRig-tit"]/dd[2]//text()')[0]
                can_use_ip.append({'http':str(ip+port)})
            except:
                    print('--fail--')
        except:
            print('fail')
    return can_use_ip

def parse_json(page):
    try:
        ip = []
        if page % 6 == 0:
            ip = getIp()
        url = 'https://capi-v2.sankakucomplex.com/posts?lang=english&page={page}&limit=20&tags=order:quality'.format(
            page=page)
        header = random_agent()
        if ip != []:
            # 随机IP访问
            p = random.choice(ip)
            print(p)
            data = requests.get(url=url, headers=header, proxies=p).json()
        else:
            data = requests.get(url=url, headers=header).json()
        for i in data:
            file_url = i['file_url']
            file_type = i['file_type']
            id = i['id']
            if re.findall('image.*', file_type) is not []:
                dl = threading.Thread(target=download.downloadFile, args=(id, file_url, ))
                dl.start()
        ip.clear()
        time.sleep(10)
        parse_json(page=page + 1)
    except:
        file = open('./error_file.txt', 'a', encoding='utf-8')
        file.write('error:%s\n' % (sys.exc_info()[0]))
        file.close()
        time.sleep(10)
        parse_json(page=page + 1)


def main():
    parse_json(page=1)


if __name__ == '__main__':
    main()
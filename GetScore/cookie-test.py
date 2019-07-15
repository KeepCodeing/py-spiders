"""
时间：2019.6.15
测试结果：失败
原因：没有专门的接口，因此不能通过formdata直接请求，验证码判断是前端通过cookie来的，因此还需要手动点击按钮才能
发送请求
可以通过设置cookie自定义验证码
"""

from selenium import webdriver as wb
import time
import requests

def cookie_test():
    path = r'C:\Users\YJSP\PycharmProjects\py-projects\spiders\chromedriver.exe'
    ch = wb.Chrome(executable_path=path)
    ch.get('http://kscx.hbee.edu.cn:9012/gk/zzjx2019')
    for i in l:
        item = i.items()
        # print(item)
        for n in item:
            if 'ValidateCode' not in n:
                continue
            print(i['value'])


def selenium_test():
    path = r'C:\Users\YJSP\PycharmProjects\py-projects\spiders\chromedriver.exe'
    ch = wb.Chrome(executable_path=path)
    ch.get('http://kscx.hbee.edu.cn:9012/gk/zzjx2019')
    cookie = ch.get_cookies()
    # 第0个数组包含了验证码， 第1个数组包含了cck_lasttime， 第二个数组包含了cck_count
    my_cookie = {}
    # print(cookie)
    for i in cookie:
        my_cookie[i['name']] = i['value']
    print(my_cookie, end='\n')
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
    }
    post_data = {
        'ksbh': '19420111870053',
        'zjhm': '420111200107280516'
    }
    r = requests.post(url='http://kscx.hbee.edu.cn:9012/gk/zzjx2019', headers=headers, cookies= my_cookie, data=post_data)
    with open('t.html', 'w', encoding='gbk') as f:
        f.write(r.text)
    # print(r.text)
    time.sleep(6000)


def requests_test():
    # User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36
    url = 'http://kscx.hbee.edu.cn:9012/gk/zzjx2019'
    headers = {
        'User-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
    }


    print( requests.get(url=url, headers=headers).cookies)


def selenium_cookies():
    path = r'C:\Users\YJSP\PycharmProjects\py-projects\spiders\chromedriver.exe'
    ch = wb.Chrome(executable_path=path)

    ch.get('http://kscx.hbee.edu.cn:9012/gk/zzjx2019')

    time.sleep(1)

    cookie = {
        'name':'ValidateCode',
        'value':'114514'
    }

    ch.add_cookie(cookie)
    time.sleep(10000)
if __name__ == '__main__':
    selenium_cookies()
    # requests_test()
    # selenium_test()
    # cookie_test()
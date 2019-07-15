"""
作者:hwz
时间:2019.6.9 AM 11:27
功能:查询技能高考成绩

更新
时间：2019.6.15
通过selenium的get_cookies方法获取验证码
add_cookie可实现自定义验证码
"""

from selenium import webdriver
# import requests
import time


def creat_zkz():
    f = open('准考证.txt', 'a')
    for i in range(19420111870047, 19420111870088):
        f.writelines(str(i)+'\n')


def read_info():
    f = open('准考证.txt', 'r')
    t = f.readlines()
    zkz = []
    for i in t:
        zkz.append(i.replace('\n', ''))
    f.close()

    f = open('身份证.txt', 'r')
    t = f.readlines()
    sfz = []
    for i in t:
        sfz.append(i.replace('\n', ''))
    f.close()

    return zkz, sfz

def check_cookies(c):
    cookies = c
    for i in cookies:
        item = i.items()
        for n in item:
            if 'ValidateCode' not in n:
                continue
            return i['value']

def WH():
    # 报名号， 身份证
    bmh, sfz = read_info()
    chromePath = r'C:\Users\YJSP\PycharmProjects\py-projects\spiders\chromedriver.exe'
    wd = webdriver.Chrome(executable_path=chromePath)
    # 文化高考
    url = 'http://58.49.47.115:8000/n_score/'
    wd.get(url)
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
    }

    file_name = input('请输入保存文件名（无需后缀）')

    for i in range(len(bmh)):
        yzm = input('请输入验证码：')
        wd.find_element_by_id('gkbmh').send_keys(bmh[i])
        wd.find_element_by_id('sfzh').send_keys(sfz[i])
        wd.find_element_by_id('yzm').send_keys(yzm)
        wd.find_element_by_id('cx').click()

        time.sleep(0.5)
        # 获取文化分以及总分

        whf = wd.find_element_by_id('result_score4').text
        zf = wd.find_element_by_id('result_totalscore').text
        name = wd.find_element_by_id('result_xm').text

        f = open(file_name + '.txt', 'a', encoding='utf-8')
        f.writelines('姓名:%s,文化:%s,总分:%s\n' % (name, whf, zf))
        f.close()

        print('姓名:%s,文化:%s,总分:%s' % (name, whf, zf))

        wd.refresh()
        time.sleep(1)

def JN():
    zkz, sfz = read_info()
    chromePath = r'C:\Users\YJSP\PycharmProjects\py-projects\spiders\chromedriver.exe'
    wd = webdriver.Chrome(executable_path=chromePath)
    # 技能高考
    url = 'http://kscx.hbee.edu.cn:9012/gk/zzjx2019'

    wd.get(url=url)

    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
    }
    # cookie = requests.get(url='http://kscx.hbee.edu.cn:9012/Validate/GetValidateCode', headers=headers)
    # print(cookie.cookies)
    yzm = check_cookies(wd.get_cookies())

    file_name = input('请输入保存文件名（无需后缀）')

    for i in range(len(zkz)):
        wd.find_element_by_xpath('//input[@id="ksbh"]').send_keys(zkz[i])
        wd.find_element_by_xpath('//input[@id="zjhm"]').send_keys(sfz[i])
        wd.find_element_by_xpath('//input[@id="Yzm"]').send_keys(yzm)
        wd.find_element_by_xpath('//input[@id="btnSubmit"]').click()


        time.sleep(0.5)

        xm = wd.find_element_by_xpath('//div[@id="msg"]//tr[2]/td[2]').text
        yz = wd.find_element_by_xpath('//div[@id="msg"]//tr[2]/td[3]').text
        yh = wd.find_element_by_xpath('//div[@id="msg"]//tr[2]/td[4]').text
        zf = wd.find_element_by_xpath('//div[@id="msg"]//tr[2]/td[5]').text


        f = open(file_name + '.txt', 'a', encoding='utf-8')
        f.writelines('姓名:%s,应知:%s,应会:%s,总分:%s\n' % (xm, yz, yh, zf))
        f.close()

        print('姓名:%s,应知:%s,应会:%s,总分:%s' % (xm, yz, yh, zf))

        # wd.refresh()
        time.sleep(1)

        yzm = check_cookies(wd.get_cookies())

if __name__ == '__main__':
    WH()
    # main()
    # creat_zkz()
    # read_info()
"""
作者:hwz
时间:2019.6.9 AM 11:27
功能:查询技能高考成绩
"""

from selenium import webdriver
# import requests
import time


def creat_zkz():
    f = open('准考证.txt', 'a')
    for i in range(19420111870047, 19420111870074):
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


def main():
    zkz, sfz = read_info()
    chromePath = r'chromedriver.exe'
    wd = webdriver.Chrome(executable_path=chromePath)
    url = 'http://kscx.hbee.edu.cn:9012/gk/zzjx2019'

    wd.get(url=url)

    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
    }
    # cookie = requests.get(url='http://kscx.hbee.edu.cn:9012/Validate/GetValidateCode', headers=headers)
    # print(cookie.cookies)

    for i in range(len(zkz)):
        yzm = input('输入验证码:')

        wd.find_element_by_xpath('//input[@id="ksbh"]').send_keys(zkz[i])
        wd.find_element_by_xpath('//input[@id="zjhm"]').send_keys(sfz[i])
        wd.find_element_by_xpath('//input[@id="Yzm"]').send_keys(yzm)
        wd.find_element_by_xpath('//input[@id="btnSubmit"]').click()

        time.sleep(0.5)

        xm = wd.find_element_by_xpath('//div[@id="msg"]//tr[2]/td[2]').text
        yz = wd.find_element_by_xpath('//div[@id="msg"]//tr[2]/td[3]').text
        yh = wd.find_element_by_xpath('//div[@id="msg"]//tr[2]/td[4]').text
        zf = wd.find_element_by_xpath('//div[@id="msg"]//tr[2]/td[5]').text

        f = open('成绩统计.txt', 'a', encoding='utf-8')
        f.writelines('姓名:%s,应知:%s,应会:%s,总分:%s\n' % (xm, yz, yh, zf))
        f.close()

        print('姓名:%s,应知:%s,应会:%s,总分:%s' % (xm, yz, yh, zf))

        wd.refresh()


if __name__ == '__main__':
    main()
    # creat_zkz()
    # read_info()
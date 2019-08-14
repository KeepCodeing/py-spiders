# -*- coding: utf-8 -*-
"""
@PC YJSP
@FileName info_spider
@Author hwz
@Date 2019/8/3 11:48
@ProjectName py-projects
-------功能-------
查询录取情况
-------坑-------
没有及时保存文件，程序异常退出就得重来
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from lxml import etree


class AdmissionClass():
    def __init__(self):
        '''
        打开页面
        '''
        self.ch = webdriver.Chrome(executable_path=r"C:\Users\YJSP\PycharmProjects\py-projects\spiders\chromedriver.exe")
        self.ch.get('https://cx.e21.cn/')
        self.wait = WebDriverWait(self.ch, 10)

    @staticmethod
    def read_info():
        '''
        读取信息
        :return:准考证和生日的元组
        '''
        l = []
        with open(r'C:\Users\YJSP\PycharmProjects\py-projects\spiders\Admission\身份证.txt', 'r') as f:
            l = f.readlines()
        sr = [i.replace('\n', '')[8:14] for i in l]
        with open(r"C:\Users\YJSP\PycharmProjects\py-projects\spiders\Admission\准考证.txt", 'r') as f:
            l = f.readlines()
        zkz = [i.replace('\n', '') for i in l]
        zipper = zip(zkz, sr)
        return zipper

    def wait_load(self):
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#ksh")))
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#sfzh')))
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#verify')))
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                    'body > table:nth-child(3) > tbody > tr:nth-child(1) > td:nth-child(1) > table > tbody > tr:nth-child(3) > td > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > div > input[type="submit"]:nth-child(2)')))
        self.ksh = self.ch.find_element_by_xpath('//input[@id="ksh"]')
        self.sfzh = self.ch.find_element_by_xpath('//input[@id="sfzh"]')
        self.verify = self.ch.find_element_by_xpath('//input[@id="verify"]')
        self.bt = self.ch.find_element_by_xpath('//input[@value="录取状态查询"]')

    def input_info(self):
        info = self.read_info()

        for i in info:
            f = open('./info.txt', 'a')
            self.wait_load()
            self.ksh.send_keys(i[0])
            self.sfzh.send_keys(i[1])
            self.verify.click()
            self.yzm = input("请输入验证码：")
            self.verify.send_keys(self.yzm)
            self.bt.click()
            sleep(1)
            source = self.ch.page_source
            html = etree.HTML(source)
            tr = html.xpath('//tr[@bgcolor="#FFFFFF"]')
            temp_str = ''
            try:
                for i in tr[1:7]:
                    text = i.xpath('td/text()')
                    temp_str += text[0]+":"+text[1]+';'
                print(temp_str)
                f.writelines(temp_str+'\n')
                f.close()
            except:
                print("查询失败")
            self.ch.find_element_by_css_selector('body > table:nth-child(3) > tbody > tr > td > table > tbody > tr:nth-child(2) > td:nth-child(2) > table > tbody > tr:nth-child(2) > td > table > tbody > tr > td > table > tbody > tr:nth-child(9) > td > a:nth-child(2)').click()
            sleep(1)


def main():
    l = AdmissionClass()
    l.input_info()


if __name__ == '__main__':
    main()
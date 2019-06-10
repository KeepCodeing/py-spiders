from selenium import webdriver as wb
import requests
import time


class LoginTieBa():
    def __init__(self):
        # Session() 类
        # session() 方法
        # sessions 模块

        self.s = requests.Session()

    def login(self):
        chrome_path = r'C:\Users\YJSP\PycharmProjects\py-projects\spiders\chromedriver.exe'
        ch = wb.Chrome(executable_path=chrome_path)
        url = 'https://tieba.baidu.com/index.html'
        ch.get(url=url)
        ch.find_element_by_xpath('//div[@class="u_menu_item"]/a[@rel="noreferrer"and@href="#"]').click()
        time.sleep(3)
        ch.find_element_by_xpath('//p[@id="TANGRAM__PSP_10__footerULoginBtn"]').click()
        time.sleep(0.5)
        zh = input('请输入账号:')
        ch.find_element_by_xpath('//input[@id="TANGRAM__PSP_10__userName"]').send_keys(zh)
        mm = input('请输入密码:')
        ch.find_element_by_xpath('//input[@id="TANGRAM__PSP_10__password"]').send_keys(mm)
        ch.find_element_by_xpath('//input[@id="TANGRAM__PSP_10__submit"]').click()

        self.cookies = ch.get_cookies()

        f = open('cookie.txt', 'w')
        f.writelines(str(self.cookies))
        f.close()

    def set_cookie(self):
        # final_cookies = {}
        for i in self.cookies:
            self.s.cookies.set(i['name'], i['value'])

        print(self.s.cookies)
        time.sleep(10)
    def get_main_page(self):
        headers = {
            'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
        }
        self.s.headers = headers
        print(self.s.cookies)
        data = self.s.get(url='http://tieba.baidu.com/home/main?id=02d9e5baa6e5a898e6af92e5a5b6df91?t=1534864095&fr=userbar&red_tag=c2071425957').content

        with open('t.html', 'wb') as f:
            f.write(data)


def main():
    Log = LoginTieBa()
    Log.login()
    Log.set_cookie()
    Log.get_main_page()



if __name__ == '__main__':
    main()

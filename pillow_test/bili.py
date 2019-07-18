# -*- coding: utf-8 -*-
"""
@PC YJSP
@FileName test
@Author hwz
@Date 2019/7/17 15:35
@ProjectName py-projects
-------功能-------
登录bilibili
-------遇到的坑--------
1. ActionChains对象会自动累计偏移量，需要通过重新创建一个的方式来清除偏移量
2. ActionChains对象在登录失败后没有重置，导致抛出获取不到元素的错误
3. requests的cookie传递错误，参考：https://blog.csdn.net/williamgavin/article/details/81390014
-------完成时间--------
总计耗时：6.5±0.5h
2019/7/18 10:56
"""
import time
import random
import json
import requests
from PIL import Image
from selenium import webdriver as wb
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class uidError(Exception):
    pass


class ImgTreat():
    def __init__(self, path='./'):
        self.path = path

    def cutImg(self, pos, name):
        '''
        截取图片并保持
        :param pos: 图片位置
        :return: None
        '''
        # 打开截图
        img = Image.open(self.path + 'shot.png')
        cut = img.crop(pos)
        cut.save(self.path + name)

    def computeDistance(self, masked, no_masked):
        '''
        计算滑块到缺口的距离
        :return:None
        '''
        # masked.size 功能：返回图片大小，数据类型：元组
        # masked.load() 功能，返回一个PixelAccess对象，可以通过[x, y]的索引方式获取指定位置的像素的值
        width = masked.size[0]
        height = masked.size[1]
        masked_rgb = masked.load()
        no_masked_rgb = no_masked.load()
        # 判断像素点不相同的阈值
        threshold = 60
        # 滑块距离边缘的距离
        start_x = 60
        distance = 0
        for x in range(start_x, width):
            for y in range(start_x, height):
                rgb1 = masked_rgb[x, y]
                rgb2 = no_masked_rgb[x, y]
                res1 = abs(rgb1[0] - rgb2[0])
                res2 = abs(rgb1[1] - rgb2[1])
                res3 = abs(rgb1[2] - rgb2[2])
                # 如果三个像素点相差都大于设定阈值，记录此时的x坐标并返回最终的x坐标
                if not(res1<threshold and res2<threshold and res3<threshold):
                    distance = x
        # 释放图片内存
        masked.close()
        no_masked.close()
        # 去除滑块宽度，增加缩放率
        return (distance - start_x*0.76)


class BiliTest(ImgTreat):
    def __init__(self, username, password, uid):
        super(BiliTest, self).__init__()
        self.username = username
        self.password = password
        self.uid = uid
        self.ch = wb.Chrome(executable_path=r'C:\Users\YJSP\PycharmProjects\py-projects\spiders\chromedriver.exe')
        # 最大化页面
        self.ch.maximize_window()
        self.wait = WebDriverWait(self.ch, 10)
        # 打开页面
        self.openWeb()

    def openWeb(self):
        '''
        打开页面
        :return:None
        '''
        login_url = 'https://passport.bilibili.com/login'
        self.ch.get(login_url)

    def clickLoginBt(self):
        '''
        点击登录按钮弹出验证图片后将其保存
        :return: None
        '''
        username_input = self.wait.until(EC.element_to_be_clickable((By.ID,'login-username')))
        password_input = self.wait.until(EC.element_to_be_clickable((By.ID,'login-passwd')))
        login_bt = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#geetest-wrap > ul > li.btn-box > a.btn.btn-login')))
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        login_bt.click()
        # 等待验证图片加载完毕
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'body > div.geetest_panel.geetest_wind > div.geetest_panel_box.geetest_no_logo.geetest_panelshowslide > div.geetest_panel_next > div > div.geetest_wrap')))
        self.getWebShot()
        pos = self.getPos()
        # 首先获取缺口图
        self.cutImg(pos, name='masked.png')
        # 再获取原图
        self.clearMasked()
        self.getWebShot()
        self.cutImg(pos, name='no_masked.png')
        self.reductionMasked()
        # 移动滑块
        self.moveSlider()
        # 判断是否登录成功
        time.sleep(5)
        self.isLogin()

    def reductionMasked(self):
        '''
        还原遮罩，方便查看效果
        :return: None
        '''
        self.ch.execute_script(
            'let img = document.getElementsByClassName("geetest_canvas_fullbg geetest_fade geetest_absolute")[0];'
            'img.style.display = "none";'
            'img.style.opacity = 1;')

    def clearMasked(self):
        '''
        将遮罩去掉
        :return: None
        '''
        self.ch.execute_script('let img = document.getElementsByClassName("geetest_canvas_fullbg geetest_fade geetest_absolute")[0];'
                               'img.style.display = "block";'
                               'img.style.opacity = 1;')

    def get_tracks(self, distance):
        # distance为上一步得出的总距离。20是等会要回退的像素
        distance += 20
        # 初速度为0，s是已经走的路程，t是时间
        v0 = 2
        s = 0
        t = 0.4
        # mid是进行减速的路程
        mid = distance * 3 / 5
        # 存放走的距离
        forward_tracks = []
        while s < distance:
            if s < mid:
                a = 2
            else:
                a = -3
            # 高中物理，匀加速路程的计算
            v = v0
            tance = v * t + 0.5 * a * (t ** 2)
            tance = round(tance)
            s += tance
            v0 = v + a * t
            forward_tracks.append(tance)
        # 因为回退20像素，所以可以手动打出，只要和为20即可
        back_tracks = [-1, -1, -1, -2, -2, -2, -3, -3, -2, -2, -1]  # 20
        return {"forward_tracks": forward_tracks, 'back_tracks': back_tracks}

    def moveSlider(self):
        '''
        移动滑块到缺口位置
        :return: None
        '''
        # 创建一个ActionChains对象
        self.action = ActionChains(self.ch)
        masked = Image.open('./masked.png')
        no_masked = Image.open('./no_masked.png')
        distance = self.computeDistance(masked, no_masked)
        masked.close()
        no_masked.close()
        # 获取滑块元素
        slider = self.ch.find_element_by_css_selector('body > div.geetest_panel.geetest_wind > div.geetest_panel_box.geetest_no_logo.geetest_panelshowslide > div.geetest_panel_next > div > div.geetest_wrap > div.geetest_slider.geetest_ready > div.geetest_slider_button')
        # perform()方法说明执行所有操作
        data = self.get_tracks(distance)
        forward_tracks, back_tracks = data['forward_tracks'], data['back_tracks']
        self.action.click_and_hold(slider).perform()
        print(distance)
        for i in forward_tracks:
            self.action.move_by_offset(xoffset=i, yoffset=0).perform()
            # action会自动累计偏移量，如果不新建一个就会超出预判范围
            # 参考：https://blog.csdn.net/van_brilliant/article/details/80602041
            self.action = ActionChains(self.ch)
            # 随机滑动时间
            time.sleep(random.uniform(0.02, 0.04))

        for n in back_tracks:
            self.action.move_by_offset(xoffset=n, yoffset=0).perform()
            self.action = ActionChains(self.ch)
            time.sleep(0.01)

        self.action.move_by_offset(xoffset=-3, yoffset=0).perform()
        self.action.move_by_offset(xoffset=3, yoffset=0).perform()
        time.sleep(0.2)
        # 松开鼠标
        self.action.release(slider).perform()
        print('over')

    def getWebShot(self):
        '''
        获取页面截图
        :return: None
        '''
        self.ch.save_screenshot('./shot.png')

    def getPos(self):
        '''
        获取图片位置
        :return: 图片位置
        '''
        img = self.ch.find_element_by_css_selector('body > div.geetest_panel.geetest_wind > div.geetest_panel_box.geetest_no_logo.geetest_panelshowslide > div.geetest_panel_next > div > div.geetest_wrap > div.geetest_widget > div > a > div.geetest_canvas_img.geetest_absolute')
        pos = img.location
        size = img.size
        # 计算需要截取图片的位置
        pos_range = (
            int(pos['x']),
            int(pos['y']),
            int(pos['x']+size['width']),
            int(pos['y']+size['height'])
        )
        return pos_range

    def isLogin(self):
        '''
        判断是否成功，不成功则重试
        :return:None
        '''
        url = self.ch.current_url
        print(url)
        if 'https://www.bilibili.com/' not in url:
            print('登录失败，将刷新页面重试！')
            self.ch.get('https://passport.bilibili.com/login')
            time.sleep(5)

            self.clickLoginBt()
        else:
            print('登录成功，将获取cookie并保存到本地文件！')
            cookies_list = self.ch.get_cookies()
            cookies = {k['name']:k['value'] for k in cookies_list}
            json_str = json.dumps(cookies)
            with open('cookies.json', 'w') as f:
                json.dump(json_str, f)
            self.checkCookies(self.uid)
        return None

    @staticmethod
    def checkCookies(uid):
        '''
        测试cookies是否有效
        :param uid: 用户ID
        :return:None
        '''
        if uid == None:
            raise uidError('请检查你的uid参数！')
        followers_url = 'https://api.bilibili.com/x/relation/followers?vmid={uid}&pn=19&ps=20&order=desc&jsonp=jsonp'.format(uid=uid)
        with open('cookies.json', 'r') as f:
            json_str = json.load(f)
        cookies = json.loads(json_str)
        headers = {
            'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0',
        }
        data = requests.get(url=followers_url, headers=headers, cookies=cookies)
        try:
            print('成功获取数据%s！' % (data.json()['data'], ))
        except KeyError:
            print('没有获取到数据，cookies无效可能性巨存！')


def main():
    username = input('请输入用户名：')
    password = input('请输入密码：')
    uid = input('请输入你的uid：')
    b = BiliTest(username, password, uid)
    b.clickLoginBt()
    time.sleep(10)


if __name__ == '__main__':
    main()
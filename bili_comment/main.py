"""
@PC YJSP
@FileName main
@Author hwz
@Date 2019/7/6 15:13
@ProjectName py-projects
"""
import requests
from spiders.ua import getUa
import re
import time


class BiliComment():
    def __init__(self, cookies):
        self.cookies = cookies
        self.csrf = re.findall('.*bili_jct=(.*?);', self.cookies)[0]
        self.headers = '''  Host: api.bilibili.com
                            User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0
                            Accept: application/json, text/javascript, */*; q=0.01
                            Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
                            Accept-Encoding: gzip, deflate, br
                            Content-Type: application/x-www-form-urlencoded; charset=UTF-8
                            Content-Length: 91
                            Origin: https://www.bilibili.com
                            Connection: keep-alive
                            Referer: https://www.bilibili.com/video/av{aid}'''
        self.s = requests.Session()

    def str2dict(self):
        str_temp = [i.replace(' ', '') for i in self.headers.splitlines()]
        for i in str_temp:
            self.s.headers[i.split(':', 1)[0]] = i.split(':', 1)[1]
        self.s.headers['Cookie'] = self.cookies

    def test(self, uid):
        test_headers = {
            'User-agent':getUa(),
            'Cookie':self.cookies
        }
        # 获取粉丝列表，如果携带的cookie有作用则可以获取最后的粉丝页数据，否则不行
        # https://api.bilibili.com/x/relation/followers?vmid=94649037&pn=19&ps=20&order=desc&jsonp=jsonp
        followers_url = 'https://api.bilibili.com/x/relation/followers?vmid={uid}&pn=19&ps=20&order=desc&jsonp=jsonp'.format(uid=uid)
        data = requests.get(url=followers_url, headers = test_headers, ).json()
        print(data['data'])

    def addComment(self, aid, message):
        if not self.csrf:
            print('csrf验证字段不存在，请检查cookie是否正确！')
            return False
        comment_url = 'https://api.bilibili.com/x/v2/reply/add'
        data = {
            'oid': aid,
            'type': 1,
            'message': message,
            'plat': 1,
            'jsonp': 'jsonp',
            'csrf': self.csrf,
        }
        self.s.headers['Referer'].format(aid=aid)
        self.s.headers['User-Agent'] = getUa()
        status = self.s.post(url=comment_url, data=data)
        code = status.json()['code']
        file = open('./log.txt', 'a', encoding='utf-8')
        if code == 0:
            file.writelines('av%s发表评论成功！\n' % (aid,))
        else:
            file.writelines('av%s发表评论失败！失败原因:%s\n' % (aid, status.text))
        file.close()


def main():
    cookies = "LIVE_BUVID=AUTO9915600470124491; sid=55nohyp9; DedeUserID=94649037; DedeUserID__ckMd5=10835a8c017fc787; SESSDATA=d80b7a7f%2C1562639060%2C83215b61; bili_jct=29ab299a7c74e0838ba0dff06a6241e5; UM_distinctid=16b3a0d67b22ee-031481412c408-5f123917-1fa400-16b3a0d67b3684; rpdid=|(u||uk|YRRY0J'ulY||lJ|u~; CURRENT_QUALITY=112; _uuid=CCCA821A-FFBD-AA9C-429F-17914E7AE60A71619infoc; finger=b3372c5f; fts=1560597732; buvid3=45AC73FC-C448-49D8-81B2-09277DA0B00D40766infoc; CURRENT_FNVAL=16; stardustvideo=1; bp_t_offset_94649037=272942500196132098"
    comment = BiliComment(cookies=cookies)
    comment.str2dict()
    for i in range(10000):
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        aid = str(i+1)
        comment.addComment(aid, '现在是:'+ now + '我在av' + aid + '留下了自己的脚印...')
        time.sleep(10)


if __name__ == '__main__':
    main()
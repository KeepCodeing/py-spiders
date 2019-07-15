"""
作者:hwz
时间:2019.6.9 AM 11:27
功能:查询技能高考成绩
"""


from lxml import etree
import requests


class GetScore():
    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36',
            'Cookie':'ValidateCode={v_code}'
        }

    def get_ValidateCode(self):

        headers = {
            'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
        }

        data = requests.get(url='http://kscx.hbee.edu.cn:9012/Validate/GetValidateCode', headers=headers)

        print(data.cookies)

        return data.cookies['ValidateCode']

    def post_info(self):

        v_code = self.get_ValidateCode()

        self.headers['Cookie'] = self.headers['Cookie'].format(v_code=str(v_code))

        print(self.headers['Cookie'])

        post_data = {
            'ksbh':'19420111870053',
            'zjhm':'420111200107280516'
        }

        # //span[@class="s3"]/img/@src


        ret_data = requests.post(url=self.url, headers=self.headers, data=post_data).text

        with open('t.html', 'w', encoding='utf-8') as f:
            f.write(ret_data)

        print(ret_data)

        pass
    pass

def test():
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
    }
    data = requests.get(url='http://kscx.hbee.edu.cn:9012/Validate/GetValidateCode', headers=headers)

    print(data.cookies['ValidateCode'])

    # with open('t2.html', 'w', encoding='gbk') as f:
    #     f.write(data)

    pass


def main():
    # test()
    s = GetScore()

    s.post_info()

    pass


if __name__ == '__main__':
    main()
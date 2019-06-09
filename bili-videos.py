import requests
import json
import re


class Download_bili_videos():
    def __init__(self, url):
        post_url = 'https://www.parsevideo.com/api.php'

        hash = '747104eb3e590eb1b2e67a557138f877'

        post_data = {
            'hash': hash,
            'url': url
        }

        headers = {
            'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
        }
        self.ret_data = json.loads(requests.post(url=post_url, data=post_data, headers=headers).text)

    def parse_video(self):
        if 'video' not in self.ret_data.keys():
            print('获取失败')
            return 0
        video = self.ret_data['video'][0]
        url = video['url']
        desc = re.findall('<.+>(.+)<.+>', video['desc'])[0]
        print('---获取%s成功---' % (desc, ))
        title = desc.split('/')[2]
        return (title, url)
# https://api.bilibili.com/playurl?callback=callbackfunction&aid=53601561&page=1&platform=html5&quality=1&vtype=mp4&type=jsonp

def main():
    d = Download_bili_videos(url='https://www.bilibili.com/video/av53601561')

    title, url = d.parse_video()

    data = requests.get(url=url).content

    with open('./'+title + '.mp4', 'wb') as f:
        f.write(data)

    print('---下载%s完成---' % (title, ))

if __name__ == '__main__':
    main()


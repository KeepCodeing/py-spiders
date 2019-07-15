import requests
import time


def downloadFile(name, url):
    headers = {'Proxy-Connection': 'keep-alive'}
    r = requests.get(url, stream=True, headers=headers)
    length = float(r.headers['content-length'])
    f = open('./imgs/'+str(name) + '.png', 'wb')
    count = 0
    count_tmp = 0
    time1 = time.time()
    for chunk in r.iter_content(chunk_size=512):
        if chunk:
            f.write(chunk)
            count += len(chunk)
            if time.time() - time1 > 2:
                p = count / length * 100
                speed = (count - count_tmp) / 1024 / 1024 / 2
                count_tmp = count
                print(str(name) + ': ' + formatFloat(p) + '%' + ' Speed: ' + formatFloat(speed) + 'M/S')
                time1 = time.time()
    f.close()
def formatFloat(num):
    return '{:.2f}'.format(num)

def main():
    downloadFile('1.png', 'https://cs.sankakucomplex.com/data/5e/8b/5e8bad2519322549baa43646a9c6911d.jpg?e=1562119200&m=IR4HXJPnSmWESQ89zZovBQ')

if __name__ == '__main__':
    main()
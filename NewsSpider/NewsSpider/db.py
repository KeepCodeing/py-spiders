"""
@PC YJSP
@FileName db
@Author hwz
@Date 2019/7/4 15:08
@ProjectName py-projects
"""
import pymysql


def connectDb():
    return pymysql.connect(user='hwz', password='114514', database='vueweb', port=3306, host='118.89.88.245', charset='utf8')


if __name__ == '__main__':
    print(connectDb())
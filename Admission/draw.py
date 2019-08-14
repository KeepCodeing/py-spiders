# -*- coding: utf-8 -*-
"""
@PC YJSP
@FileName draw
@Author hwz
@Date 2019/8/3 13:16
@ProjectName py-projects
-------功能-------
绘制录取情况
"""
import seaborn as sns
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import rc


def draw():
    font = {
        'family': 'MicroSoft YaHei',
        'weight': 'normal',
        'size': 13
    }
    rc('font', **font)
    l = []
    with open(r'C:\Users\YJSP\PycharmProjects\py-projects\spiders\Admission\info.txt', 'r') as f:
        l = f.readlines()
    info = [i.split(';')[2:-1] for i in l]
    info_list = []
    for i in info:
        temp_dict = {}
        for j in i:
            split_str = j.split(':')
            temp_dict[split_str[0]] = split_str[1]
        info_list.append(temp_dict)
    df = pd.DataFrame(info_list)
    plt.figure(figsize=(15, 15), dpi=80)
    plt.subplot(3, 1, 2)
    plt.title('录取院校')
    sns.countplot(y='院校名称', data=df)
    plt.xlabel('录取人数')
    plt.subplot(3, 2, 1)
    plt.title('专业名称')
    sns.countplot(y='专业名称', data=df)
    plt.xlabel('录取人数')
    plt.subplot(3, 2, 2)
    plt.title('考生状态')
    sns.countplot(y='考生状态', data=df)
    plt.xlabel('人数')
    plt.subplot(3, 1, 3)
    plt.title('层次名称')
    sns.countplot(y='层次名称' , data=df)
    plt.xlabel('人数')

    plt.show()


def main():
    draw()


if __name__ == '__main__':
    main()
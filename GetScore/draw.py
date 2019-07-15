from matplotlib import pyplot as plt
import re


def main():
    file_name = input('请输入要打开的文本名(无需后缀)')
    f = open(file_name + '.txt', 'r', encoding='utf-8')
    l = f.readlines()
    f.close()
    cj = []
    for i in l:
        cj.append(i.replace('\n', ''))

    DrawData(cj)


def DrawData(cj):
    info = {}

    for i in cj:
        name = re.findall('姓名:(..|...),', i)[0]
        zf = re.findall('总分:(\d+)', i)[0]
        info[name] = int(zf)

    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
    plt.figure(figsize=(19.80, 10.24))
    plt.xlabel('姓名')
    plt.ylabel('总分')
    title = input('请输入标题')
    plt.title(title)

    # 排序
    res = sorted(info.items(), key=lambda info: info[1], reverse=True)
    sorted_dic = {}
    for i in res:
        sorted_dic[i[0]] = i[1]
    ret = plt.bar(list(sorted_dic.keys()), list(sorted_dic.values()), width=0.5, align='center', color='#8FBC8F')

    # 不排序
    # ret = plt.bar(list(info.keys()), list(info.values()), width=0.5, align='center', color='#8FBC8F')

    # 设置顶部文字
    for s in ret:
        height = s.get_height()
        plt.text(s.get_x() + s.get_width() / 2, height + 1, str(height), ha="center", va="bottom")

    plt.show()


if __name__ == '__main__':
    main()
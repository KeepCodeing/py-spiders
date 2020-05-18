"""
作者：hwz
时间：2020/5/13 19:33
功能：数据可视化
"""
from matplotlib import pyplot as plt
def showData(data, course_list):
    print("".ljust(19) + "绘制表格中，请稍等...")
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
    tot_score = data.getSumScore()
    arr_score = data.getArrScore()
    max_score = data.getMaxScore()
    min_score = data.getMinScore()
    plt.figure(figsize=(19.80, 10.24))
    # 绘制总分表
    plt.subplot(2, 2, 1)
    plt.title("总分表")
    plt.xlabel("课程名称")
    plt.ylabel("总分数")
    plt.grid()
    vl = list(tot_score.values())
    plt.plot(course_list, vl, color="cornflowerblue", marker="o")
    for p in range(3): plt.text(p - 0.05, vl[p] + 19, vl[p], color="slategrey")
    # 绘制均分表
    plt.subplot(2, 2, 2)
    plt.title("均分表")
    plt.ylabel("课程名称")
    plt.xlabel("平均分值")
    vl = list(arr_score.values())
    plt.barh(course_list, vl, color="cyan")
    for p in range(3): plt.text(vl[p] + 6, p - 0.1, vl[p], color="springgreen", rotation=270)
    # 绘制最高/低分表
    plt.subplot(2, 1, 2)
    plt.title("最高/低分表")
    plt.xlabel("课程名称")
    plt.ylabel("最高/低分值")
    max_vl = [i[0] for i in max_score.values()]
    min_vl = [i[0] for i in min_score.values()]
    pos = [i for i in range(0, 3)]
    wid = 0.25
    max_bt = plt.bar(pos, max_vl, width=wid, color="deepskyblue")
    for i in range(3): pos[i] += wid
    min_bt = plt.bar(pos, min_vl, width=wid, color="red")
    pos = [i + 0.1 for i in range(3)]
    plt.xticks(pos, course_list)
    for min_t in min_bt:
        height = min_t.get_height()
        plt.text(min_t.get_x() + wid / 2 - 0.01, height + 13, height, color="crimson")
    for max_t in max_bt:
        height = max_t.get_height()
        plt.text(max_t.get_x() + wid / 2 - 0.01, height + 13, height, color="c")
    plt.savefig("./table.png") # 得先保存，不然plt对象刷新了就只能保存空白图片了
    plt.show()
    input("".ljust(19) + "表格绘制完成！已保存到当前目录下的table.png，请按任意键继续...")
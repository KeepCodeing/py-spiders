"""
作者：hwz
时间：2020/5/12 13:01
功能：简单汇总分析学生数据
"""

class Marina(object):
    def __init__(self, data, course_list):
        self.data = data
        self.sum_dict = {}
        self.max_dict = {}
        self.min_dict = {}
        for i in course_list:
            self.sum_dict[i] = .0
            self.max_dict[i] = (.0, 0)
            self.min_dict[i] = (3777.0, 0)
        self.__cmpSumScore()
        self.__cmpTopScore()

    # 计算每门成绩的总和，同时可以通过该字典获取平均分
    def __cmpSumScore(self):
        for val in self.data["score"].values():
            for c in val:
                self.sum_dict[c] += float(val[c])

    # 获取每门成绩的总和
    def getSumScore(self):
        return self.sum_dict

    # 获取每门成绩平均分，均分四舍五入保留两位小数
    def getArrScore(self):
        return {i[0]: round(i[1] / len(self.data["score"]), 2) for i in self.sum_dict.items()}

    # 获取最高分最低分学生学号以及成绩
    def __cmpTopScore(self):
        for tup in self.data["score"].items(): # 拿到成绩元组
            for cor in tup[1]: # 遍历元组里的values，cor是key，也就是课程名称
                # 依次对比成绩，先放成绩，后放学号
                if float(self.max_dict[cor][0]) < float(tup[1][cor]): self.max_dict[cor] = (float(tup[1][cor]), tup[0])
                if float(self.min_dict[cor][0]) > float(tup[1][cor]): self.min_dict[cor] = (float(tup[1][cor]), tup[0])

    def getMaxScore(self):
        return self.max_dict

    def getMinScore(self):
        return self.min_dict
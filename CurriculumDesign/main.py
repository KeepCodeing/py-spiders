from prettytable import PrettyTable as pt
from marina import Marina as udk
from show import showData
import json

# dump/load：文件操作 dumps/loads：对象转字符串

# 选项文本
menu = ["打印学生表", "增加/更改学生信息", "删除学生信息", "查询学生信息", "保存数据", "数据统计", "数据可视化", "退出系统"]
# 操作码对应的方法的字符串
orderMap = {1: "print", 2: "insert", 3: "delete", 4: "select", 5: "updateData", 6: "alaData", 7: "showData"}
# 学生信息列表
lt = ["学号", "姓名", "性别", "年级", "英语成绩", "高数成绩", "电工成绩", "总分"]

class Student(object):
    # 创建类的时候加载本地数据
    def __init__(self):
        try:
            # 读入学生信息
            with open("data.json", "r") as f: self.data = json.load(f)
            print("".ljust(38) + "欢迎回来，数据加载成功！")
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            # 可能文本内容不是json格式,第一次运行文件可能不存在
            open("data.json", "w").close()
            self.data = {"info": {}, "score": {}, "tot_score": {}}
        self.u = udk(self.data, lt[4:7]) # 实例化数据统计类

    # 检查数据是否为空
    def isDataEmpty(self):
        return not len(self.data["info"]) or not len(self.data["score"])

    # 更新本地数据
    def updateDataStudent(self):
        flag = input("".ljust(19) + "保存数据会覆盖原有数据，确定保存吗？(任意键/N)")
        if flag == "N":
            print("".ljust(19) + "取消成功！")
            return 0
        if self.isDataEmpty():
            print("".ljust(19) + "数据为空，请先输入数据！")
            return 0
        try:
            with open("data.json", "w") as f: json.dump(self.data, f)
        except IOError:
            print("".ljust(19) + "数据保存失败！")
            return 0
        input("".ljust(19) + "数据保存成功！")
        input("".ljust(19) + "按任意键继续...")

    #打印学生表
    def printStudent(self):
        if self.isDataEmpty():
            print("".ljust(19) + "表格为空，请先添加数据！")
            return 0
        # 降序输出成绩表
        sortedList = sorted(self.data["tot_score"].items(), key=lambda item: item[1], reverse=True)
        # 打印一次表头
        table = pt(lt)
        table.align[lt[1]] = "l"
        table.border = False
        table.add_row(lt)
        # 小BUG，这里不能单独输出表头，因此得多加一行单独输出
        print("".ljust(19) + table.get_string().splitlines()[1])
        for k in sortedList: self.printStudentInfoLine(k[0], True)
        input("".ljust(19) + "按任意键继续...")

    # 增加学生信息
    def insertStudent(self):
        print("".ljust(19) + "提示:无内容默认值为“空”")
        try:
            suid = input("".ljust(19) + "请输入学号：")
            if int(suid) < 1:
                print("".ljust(19) + "学号必须大于等于1！")
                return 0
        except ValueError:
            print("".ljust(19) + "格式错误!")
            return 0
        # 如果该学生不存在，则创建新的信息列表，否则在原有信息列表进行修改，即更新
        flag = suid not in self.data["info"].keys() or suid not in self.data["score"].keys()
        if flag:
            # 此处不可使用一个list对象，不然共用一个内存地址
            # 改成dict了，因为list不能做映射，那么修改数据的时候就要判断一堆下标之类的东西
            self.data["info"][suid] = {}
            self.data["score"][suid] = {}
        totScore = 0
        for i in range(1, len(lt) - 1):
            # 根据学号存入学生信息
            if i <= 3: tKey = "info"
            else: tKey = "score"
            temp = input("".ljust(19) + "请输入" + lt[i] + ":")
            if not temp and flag: temp = "空" # 如果该学生不存在且输入为空设置默认值
            elif not temp and not flag: continue # 如果输入为空但学生存在则不作更改
            self.data[tKey][suid][lt[i]] = temp
        for i in self.data["score"][suid].values(): totScore += float(i) # 计算总分
        self.data["tot_score"][suid] = totScore
        self.u = udk(self.data, lt[4:7]) # 学生成绩是会改变的，因此需要多次实例化
        input("".ljust(19) + "按任意键继续...")

    # 删除学生信息
    def deleteStudent(self):
        # 学生不存在
        suid = self.selectStudent(isprint=False)
        if suid is None: return 0
        self.data["info"].pop(suid)
        self.data["score"].pop(suid)
        self.u = udk(self.data, lt[4:7])
        input("".ljust(19) + "删除学号为" + str(suid) + "的学生成功...")
        input("".ljust(19) + "按任意键继续...")

    # 打印学生成绩情况
    def printStudentScore(self, info, tb_name):
        print("".ljust(24) + tb_name.center(45, "*"))
        tb = pt(list(info.keys()))
        tb.border = False
        if tb_name in "总分" or tb_name in "平均分":
            tb.add_row(list(info.values()))
        else:
            tb.add_row([self.data["info"][str(val[1])]["姓名"] for val in info.values()]) # 先输出姓名，再输出成绩
            tb.add_row([val[0] for val in info.values()])
        for s in tb.get_string().splitlines(): print("".ljust(37) + s)
        input("".ljust(23) + ">按任意键继续<".center(43))

    # 学生成绩统计
    def alaDataStudent(self):
        if self.isDataEmpty():
            print("".ljust(19) + "数据为空！")
            return 0
        # 依次打印总分，平均分，最高分，最低分
        self.printStudentScore(self.u.getSumScore(), "总分")
        self.printStudentScore(self.u.getArrScore(), "平均分")
        self.printStudentScore(self.u.getMaxScore(), "最高分")
        self.printStudentScore(self.u.getMinScore(), "最低分")

    # 打印一行学生信息
    def printStudentInfoLine(self, suid, flag=False):
        table = pt(lt)
        table.align[lt[1]] = "l"
        row = [suid] + list(self.data["info"][suid].values()) + list(self.data["score"][suid].values()) + \
              [self.data["tot_score"][suid]]
        table.add_row(row)
        # 去掉边框，因为边框存在布局错误，再转换为字符串逐行对齐输出
        table.border = False
        # 通过多次调用逐行打印学生成绩达到打印整个表的效果，但是只能输出一次表头
        for s in table.get_string().splitlines():
            if flag: # 如果执行的是打印整个表，则不会打印表头
                flag = not flag
                continue
            print("".ljust(19) + s)

    # 选择学生信息
    def selectStudent(self, isprint=True):
        suid = input("".ljust(19) + "请输入学生学号:")
        # 提供两种查询模式，一种是打印学生信息，一种是用来判断当前学生是否存在
        if suid not in self.data["info"].keys() or suid not in self.data["score"].keys():
            print("".ljust(19) + "该学生不存在！")
            return None
        if not isprint: return suid # 如果是不打印模式这个方法做的就是查询下学生是否存在
        self.printStudentInfoLine(suid)
        input("".ljust(19) + "按任意键继续...")

    # 数据可视化
    def showDataStudent(self):
        if self.isDataEmpty():
            print("".ljust(19) + "数据为空！")
            return 0
        showData(self.u, lt[4:7])

# 打印菜单
def printMenu():
    print("*".rjust(20) + "欢迎使用学生成绩排序系统".center(45, "*"))
    # 对齐文本
    for i in range(len(menu)): print("".rjust(19) + (str(i + 1) + "." + menu[i]).rjust(25 + len(menu[i])))
    print("".ljust(19) + "*" * 57)

def printPrompt():
    print("".ljust(19), end="")
    code = -1
    try:
        code = int(input("请输入操作码："))
        # 非法数据
        if code < 1 or code > len(menu):
            code = -1
            print("".ljust(19) + "操作码非法！")
    except ValueError:
        print("".ljust(19) + "请输入整形！") # 非法输入
    return code

# 根据操作码执行对应操作
def runCode(code, student):
    if code == -1: return
    if code == len(menu):
        print("".ljust(18), "感谢使用!请选择是否保存数据!")
        student.updateDataStudent()
        exit(0)
    # student.*Student(code)，省去了很多个判断
    eval("student." + orderMap[code] + "Student()")

def main():
    # 因为在循环里无限实例化Student类导致全部操作都有问题
    student = Student()
    while True:
        printMenu()
        runCode(printPrompt(), student=student)

if __name__ == '__main__':
    main()
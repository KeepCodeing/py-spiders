import sys
import threading
#  设置最大递归次数
# sys.setrecursionlimit(9999)
# def test(n):
#     print(n)
#     test(n+1)
#     if n > 1000:
#         return
#
#
#
# def main():
#     test(0)
def b(a):
    print(a)


def main():
    r = threading.Thread(target=b, args=(1, ))
    r.start()


if __name__ == '__main__':
    main()
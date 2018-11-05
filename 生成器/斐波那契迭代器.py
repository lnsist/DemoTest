"""斐波那契迭代器
迭代器 本身 也是可迭代对象, 自身迭代自身,
在迭代方法中, 必须抛出异常 StopIteration

date: 2018-09-19
"""


# 迭代器类
class ClsIter(object):
    def __init__(self, n):
        # 需要生成的数量
        self.n = n
        # 初始化 a, b
        self.a, self.b = 0, 1
        # 初始化下标
        self.index = 0

    # 返回可迭代对象
    def __iter__(self):
        return self

    # 迭代方法, 迭代器 进行迭代
    def __next__(self):
        # 判断下标是否越界
        if self.index >= self.n:
            # 必须抛出此异常, 否则不能 foreach
            raise StopIteration
        # 获取当前a的值, 并最后进行返回
        num = self.a
        # a等于当前b, 当前b 等于a和b之和
        self.a, self.b = self.b, self.a + self.b
        # 下标自增
        self.index += 1
        # 返回
        return num


cls_iter = ClsIter(5)
for i in cls_iter:
    print(i)

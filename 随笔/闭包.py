"""
    闭包 -- 特殊的函数, 嵌套的函数
date: 2018-10-08 09:01
"""


# 定义闭包函数
def fun1(func):
    # 定义内部函数
    def inner():
        # 进行扩展功能
        print("进行扩展功能")
        # 基础函数调用
        func()
    # 返回内函数的引用
    return inner


# 定义基础函数
def fun_():
    # 基础函数操作
    print("调用基础函数")


# 定义 fun2 的引用
fun_ = fun1(fun_)
# 调用
fun_()

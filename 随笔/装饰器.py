"""
    装饰器 -- 本质还是闭包, 只是简化了 基础函数的定义
date: 18-10-8 下午3:44
"""

# 定义闭包函数
from functools import wraps


# 自定义参数装饰器
def fun1(ab):
    def inner2(func):
        # 此注解, 不替换原函数
        @wraps(func)
        # 定义内部函数
        def inner1():
            # 自定义参数
            print("自定义参数", ab)
            # 进行扩展功能
            print("进行扩展功能")
            # 基础函数调用
            func()

        # 返回内函数的引用
        return inner1

    # 返回内函数的引用
    return inner2


# 多个装饰器
def fun2(func):
    def inner1():
        # 多个装饰器扩展功能
        print("多个装饰器扩展功能")
        # 基础函数调用
        func()

    # 返回内函数的引用
    return inner1


@fun2
# 简化定义
@fun1("哈哈")
# 定义基础函数
def fun_():
    # 基础函数操作
    print("调用基础函数")


# 定义 fun2 的引用
# fun_ = fun1(fun_)
# 调用
fun_()

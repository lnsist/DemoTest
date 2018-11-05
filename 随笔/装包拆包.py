"""
    装包和拆包
date: 2018-10-08 09:00
"""


# 自定义函数, 展示 装包后的实参数据
def fun(*args, **kwargs):
    print(args)
    print(kwargs)


# 数组 -- 位置实参
a = (1, 2, 3, 4)
# 字典 -- 命名实参
b = {"a": 1, "b": 2}

# 不拆包传参, 相当于传入 2 个位置参数
fun(a, b)
# 分割线
print("我是一条分割线".center(30, "-"))
# 拆包传参, a 拆包成len(a)个位置参数, b 拆包成len(b)个命名参数
fun(*a, **b)

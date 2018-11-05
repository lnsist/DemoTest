"""
秒表: 输入回车记录一次时间, 计算前后时间差, 获取单圈秒数, 统计总共时长
"""
import time
# 开始计时
input("输入回车开始计时")
# 开始计时时间
start_time = time.time()
last_time = start_time
# 圈数计数
i = 1
# 循环计时
while True:
    # 当前单圈计时
    end = input("输入回车记录单圈时间(输入out结束计时)")
    # 计算当前单圈计数时间
    lap_time = round(time.time() - last_time, 2)
    # 计算总时长
    total_time = round(time.time() - start_time, 2)
    # 记录当前单圈的时间
    last_time = time.time()
    print(("第 %s 圈" % i).center(50, "="))
    print(("单圈计数为: %s 秒 ****  总时间为: %s 秒" % (lap_time, total_time)).center(40, " "))
    i += 1
    if end.lower() == "out":
        break


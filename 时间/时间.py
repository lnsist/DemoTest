"""

"""
import time, datetime

"""
    time
    获取当前时间戳 - 纪元时间戳, 从1970年01月01日00点 开始
"""
# 可用于时间的对比以及时间的计算
print("当前时间戳:", time.time())
print("".center(50, "="))
# 睡眠(x)秒
# time.sleep(1)
"""
    datetime
    更方便的格式显示日期, 对日期进行算术运算    
"""
# 格式化输出当前时间
print("格式化显示当前日期:", datetime.datetime.now())
print("".center(50, "="))
# 手动设置时间, 自动转换格式
dt = datetime.datetime(2015, 10, 21, 16, 29, 0)
# 转换后的格式
print("格式化显示指定日期:", dt)
# 对象.属性
print("dt.year:", dt.year, "\tdt.moth:", dt.month, "\tdt.day:", dt.day)    # (2015, 10, 21)
# 对象.属性
print("dt.hour:", dt.hour, "\tdt.minute:", dt.minute, "\tdt.second:", dt.second)    # (16, 29, 0)
print("".center(50, "="))
"""格式化 时间戳    - fromtimestamp()"""
# Unix 纪元后 1000000 秒
print("Unix 纪元后 1000000 秒: ", datetime.datetime.fromtimestamp(1000000))
print("".center(50, "="))
# 当前时间戳
print("当前时间戳: ", datetime.datetime.fromtimestamp(time.time()))
print("".center(50, "="))
"""
    timedelta 数据类型
    表示一段时间段, 不是一个时刻,
    将一段时间段转换为秒数 或 天数
"""
delta = datetime.timedelta(days=11, hours=10, minutes=9, seconds=8)
print(delta.days, delta.seconds, delta.microseconds)
print(delta.total_seconds())
print(delta)
print("".center(50, "="))
dt = datetime.datetime.now()
# pinrt
print("".center(50, "="))

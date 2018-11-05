"""send唤醒并传参数到生成器
生成器默认是沉睡的, 通过next和send可以唤醒生成器, 让其执行至一下次的断点处

next方法只是唤醒生成器让其执行至下次断点并接收返回值
send方法是唤醒生成器并传参至断点处, 让其执行代码

date: 2018-09-19
"""


# 文本grep生成器
def str_grep(str):
    # 循环判断
    while True:
        # 获取传入文本
        line = yield
        # 判断传入文本是否包含str
        if str in line:
            # 输出当前文本
            print(line)


# 创建生成器
search = str_grep("文本")
# 启动生成器 -- 唤醒生成器, 让其执行到断点处, 等待获取参数
search.__next__()
# 传入参数
search.send("没有")
# 传入参数
search.send("有文本了")


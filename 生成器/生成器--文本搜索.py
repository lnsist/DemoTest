"""简单文本搜索
一个生成器可以有多个yield, 使用时注意生成器中有多少个yield, 就要有多少次唤醒方法,
才能执行一次完整的运行, 注意唤醒类型

date: 2018-09-18
"""


# 简单文本搜索
def str_grep(text):
    # 死循环
    while True:
        # 挂起函数, 等待外部传参唤醒
        content = yield
        # 判断 text 是否包含在 content
        if text in content:
            # 输出
            # print(content)
            yield content


# 创建生成器
fn = str_grep("文本")
# 启动生成器
next(fn)
# 传参唤醒
request = fn.send("没有")
if request:
    print(request)
    next(fn)
# 传参唤醒
request = fn.send("有文本了")
if request:
    print(request)
    next(fn)
# 传参唤醒
request = fn.send("有文本")
if request:
    print(request)
    next(fn)

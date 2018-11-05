"""

date: 2018-09-22 12:12
"""


# 有多个类 拥有同样的方法或属性,  那么可以提取出一个父类,
# 继承 -- 子类拥有父类属性和方法,  用于 有相同方法和属性的类之间,
# 如: 网络访问不同的目录, 报错都是一致的 404  父类A  B 继承 A类  C 继承A类,  404跳转页面方法在A类中, 访问B C类报错, 自动调用A类报错
# 人类 继承 object
class RenLei(object):
    # 初始化, 需要定义name
    def __init__(self, name):
        self.name = name

    # 自我介绍
    def zwjs(self):
        print("我叫:", self.name)
        self.say()

    # 父类方法
    @staticmethod
    def say():
        print("都是我儿子")


# 小白类, 继承人类
class Xb(RenLei):
    def __init__(self, name):
        super().__init__(name)


# 小黑类, 继承人类
class Xh(RenLei):
    def __init__(self, name):
        super().__init__(name)


xb = Xb("小白")
xh = Xh("小黑")

xb.zwjs()
xh.zwjs()

# 一个对象, 多个形态
# 多态 -- 多种形态
# 个人感觉: Python本身就是多态, 如下---
# Java中, 对象的定义, 需要指明类型, String a = "str", 那么a只能是字符串形态, 不能直接转换其他形态
# 字符形态
a = "string"
# 数值形态
a = 10
# 布尔值形态
a = True

# 封装 -- 提取相同功能, 便捷开发, 简洁代码
# 如: 访问页面, 都是同一方法, 只是跳转页面时跳转到不同页面
# http://127.0.0.1:8080/a.jsp?页面=登陆
# http://127.0.0.1:8080/a.jsp?页面=注册
# 做家务功能
print("我用 = 扫把 = 做家务")
print("我用 = 拖把 = 家务")
print("我用 = 抹布 = 做家务")


# 封装 做家务 方法
def zjw(gongju):
    print("我用 =", gongju, "= 做家具")


zjw("扫把")
zjw("拖把")
zjw("抹布")

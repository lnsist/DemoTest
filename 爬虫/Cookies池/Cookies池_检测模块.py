"""
    Cookies池基本模块: -------- 与代理池类似
1. 存储模块 -- 负责存储每个账号的用户名密码以及每个账号对应的Cookies信息
2. 生成模块 -- 负责生成新的Cookies, 从存储模块获取账号密码, 模拟登录目标页面, 登录成功, 将Cookies交给存储模块保存
3. 检测模块 -- 定时检测数据库中的Cookies是否有效, 针对不同的检测连接, 逐个拿取Cookies去访问页面,
                如果能成功访问则有效, 否则删除数据库中的Cookies, 等待生成模块重新生成
4. 接口模块 -- 提供对外服务的接口, 随机返回Cookies, 提供外部使用Cookies


检测模块 -- 定时检测数据库中的Cookies是否有效, 遍历池中所有Cookies, 逐个去访问针对检测连接,
            如果访问不成功, 或跳转登陆页面, 或跳转验证页面, 则为失效, 删除数据库中的数据,
            删除数据后, 生成模块则会去模拟登陆重新生成Cookies
date: 18-10-21 上午10:40
"""
import json
import time

import requests

from 爬虫.Cookies池.Cookies池_存储模块 import RedisClient


class ValidTester(object):
    """
        检测模块 -- 父类, 子类继承实现具体的测试连接
    """

    def __init__(self, website="default"):
        # 站点
        self.website = website
        # Cookies信息表
        self.cookies_db = RedisClient("cookies", self.website)
        # 用户信息表
        self.accounts_db = RedisClient("accounts", self.website)

    def test(self, username, cookies):
        """
            子类检测连接
        :param username: 账号
        :param cookies: cookies
        :return:
        """
        raise NotImplementedError

    def run(self):
        """
            检测运行
        :return:
        """
        # 获取Cookies表全部数据
        cookies_groups = self.cookies_db.all_data()
        # 循环所有数据, 逐个访问连接
        for username, cookies in cookies_groups.items():
            # 调用子类具体检测连接
            self.test(username, cookies)


class Tester(ValidTester):
    """
        子类, 继承实现父类方法, 实现具体请求访问连接
    """

    def __init__(self, website="default"):
        """
            初始化
        :param website: 站点
        """
        # 初始化
        super(Tester, self).__init__(website=website)

    def test(self, username, cookies):
        """
            继承实现父类方法, 实现具体检测连接
        :param username: 账号
        :param cookies: cookies
        :return:
        """
        # 输出提示
        print("正在检测Cookies, 用户名", username)
        # 捕获异常
        try:
            # json格式化转为字典类型
            cookies = json.loads(cookies)
        # 类型错误
        except TypeError:
            # 输出提示
            print("Cookies 不合法", cookies)
            # 删除Cookies
            self.cookies_db.delete_data(username)
            # 输出提示
            print("删除 账号", username, "对应Cookies")
        # 捕获异常
        try:
            # 检测路径
            test_url = TESTER_MAP[self.website]
            # 请求访问, 设置Cookies, 不允许重定向
            response = requests.get(test_url, cookies=cookies, timeout=5, allow_redirects=False)
            # 如果返回状态码为200
            if response.status_code == 200:
                # 输出提示
                print("Cookies 有效", username)
            # 否则
            else:
                # 输出提示
                print(response.status_code, response.headers)
                # 输出提示
                print("Cookies 失效", username)
                # 删除Cookies
                self.cookies_db.delete_data(username)
                # 输出提示
                print("删除 账号", username, "对应Cookies")
        # 连接异常
        except ConnectionError as e:
            # 输出错误提示
            print(e)


# 测试模块子类URL字典 -- 站点: 测试路径
TESTER_MAP = {
    "weibo": "https://m.weibo.cn/"
}


def main(cycle=3):
    """
        检测模块, 主入口, 整合整个模块运行
    :param cycle: 周期
    :return:
    """
    # 循环需要测试的站点和路径
    for website in TESTER_MAP:
        # 实例化
        tester = Tester(website=website)
        # 运行测试
        tester.run()
        # 输出提示
        print("Cookies 检测完毕")
        # 删除对象
        del tester
        # 周期休眠
        time.sleep(cycle)

if __name__ == '__main__':
    # 周期
    cycle = 3
    main(cycle)
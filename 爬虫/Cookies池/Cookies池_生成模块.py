"""
    Cookies池基本模块: -------- 与代理池类似
1. 存储模块 -- 负责存储每个账号的用户名密码以及每个账号对应的Cookies信息
2. 生成模块 -- 负责生成新的Cookies, 从存储模块获取账号密码, 模拟登录目标页面, 登录成功, 将Cookies交给存储模块保存
3. 检测模块 -- 定时检测数据库中的Cookies是否有效, 针对不同的检测连接, 逐个拿取Cookies去访问页面,
                如果能成功访问则有效, 否则删除数据库中的Cookies, 等待生成模块重新生成
4. 接口模块 -- 提供对外服务的接口, 随机返回Cookies, 提供外部使用Cookies


生成模块 -- 获取账号信息表数据生成Cookies数据, 去Cookies表判断当前账号是否已生成Cookies, 只操作未生成Cookies的账号
date: 18-10-20 下午9:07
"""
import json
import time

from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from 爬虫.Cookies池.Cookies池_存储模块 import RedisClient
from 爬虫.Cookies池.模拟登陆.模拟登陆_Weibo import WeiboCookies

# 谷歌浏览器
BROWSER_TYPE = "Chrome"
# 无界面浏览器
# BROWSER_TYPE = "PhantomJS"


class CookiesGenerator(object):
    """
        生成模块 -- 父类, 子类继承实现具体的模拟登陆
    """

    def __init__(self, website="default"):
        """
            初始化, 获取数据库连接
        :param website: 数据类型 -- 站点
        """
        # 数据库连接 -- 用户信息表
        self.accounts_db = RedisClient(table_type="accounts", website=website)
        # 数据库连接 -- 用户cookies表
        self.cookies_db = RedisClient(table_type="cookies", website=website)
        # 初始化浏览器
        self.browser = self.init_browser()

    def close(self):
        """
            关闭
        :return:
        """
        # 捕获异常
        try:
            # 判断是否有浏览器
            if self.browser:
                # 输出提示
                print("关闭浏览器")
                # 关闭浏览器
                self.browser.close()
                # 删除浏览器
                del self.browser
        except TypeError:
            # 输出错误提示
            print("浏览器未打开")

    @staticmethod
    def init_browser():
        """
            通过browser参数初始化全局浏览器供模拟登录使用
        :return:
        """
        # 无界面浏览器
        if BROWSER_TYPE == 'PhantomJS':
            # 请求头
            caps = DesiredCapabilities.PHANTOMJS
            # 添加请求头
            caps["phantomjs.page.settings.userAgent"] \
                = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"
            # 设置请求头生成浏览器
            browser = webdriver.PhantomJS(desired_capabilities=caps)
            # 设置浏览器窗口大小
            browser.set_window_size(1400, 500)
        # 谷歌浏览器
        elif BROWSER_TYPE == 'Chrome':
            # 初始化谷歌浏览器
            browser = webdriver.Chrome()
        # 返回浏览器
        return browser

    def new_cookies(self, username, password):
        """
            新生成Cookies, 子类需要重写, 实现具体的登录操作
        :param username: 用户名
        :param password: 密码
        :return:
        """
        raise NotImplementedError

    @staticmethod
    def process_cookies(cookies):
        """
            处理Cookies -- 封装后用于保存
        :param cookies: 登录后的Cookies
        :return: 用户名 - Cookies, 字典型, 用户名对应的Cookies
        """
        # 自定义字典
        _dict = {}
        # 循环
        for cookie in cookies:
            # 获取用户名 对应 Cookies
            _dict[cookie['name']] = cookie['value']
        # 返回封装好的数据
        return _dict

    def run(self):
        """
            运行, 得到所有账户, 然后顺次模拟登录
        :return:
        """
        # 获取所有用户信息
        all_accounts = self.accounts_db.all_data()
        # 循环所有用户信息数据, 拆包 -- 用户名 密码
        for username, password in all_accounts.items():
            # 如果Cookies表没有当前用户名信息 -- 获取此用户名的Cookies
            if not self.cookies_db.get_data(username):
                # 输出提示
                print("正在生成Cookies -- 账号", username, "密码", password)
                # 回调(账号, 密码), 子类自定义登录
                result = self.new_cookies(username, password)
                # 成功获取
                if result.get("status") == 1:
                    # 获取cookies信息
                    cookies = self.process_cookies(result.get("content"))
                    # 输出提示
                    print("成功获取到Cookies", cookies)
                    # 保存数据库成功
                    if self.cookies_db.set_data(username, json.dumps(cookies)):
                        # 输出提示
                        print("成功保存Cookies")
                # 密码错误，移除账号
                elif result.get("status") == 2:
                    # 输出提示
                    print(result.get("content"))
                    # 删除用户信息
                    # if self.accounts_db.delete(username):
                    # 输出提示
                    # print('成功删除账号')
                # 其他情况, 如网络问题, 或服务器问题, 或别封
                else:
                    # 输出提示
                    print(result.get("content"))
        # 所有账号都有Cookies, 无需模拟登录
        else:
            # 输出提示
            print("所有账号都有Cookies")


class WeiboCookiesGenerator(CookiesGenerator):
    """
        微博模拟登陆, 继承父类实现new_cookies
    """

    def __init__(self, website='weibo'):
        """
            初始化操作
        :param website: 站点名称
        """
        # 父类初始化
        super(WeiboCookiesGenerator, self).__init__(website=website)
        # CookiesGenerator.__init__(self, website=website)
        # 保存浏览器
        self.website = website

    def new_cookies(self, username, password):
        """
            继承实现父类方法, 实现具体模拟登陆操作生成Cookies
        :param username: 用户名
        :param password: 密码
        :return: 用户名和Cookies
        """
        # 使用自定义类, 实现具体模拟登陆操作返回登录结果
        return WeiboCookies(username, password, self.browser).main()


# 生成模块子类字典 -- 站点: 实现登陆子类
GENERATOR_MAP = {
    "weibo": "WeiboCookiesGenerator"
}


def main(cycle=3):
    """
        生成模块, 主入口, 整合整个模块运行
    :param cycle: 周期
    :return:
    """
    # 循环生成模块子类字典, 获取 站点 以及 实现登陆子类
    for website, cls in GENERATOR_MAP.items():
        # 拼接表达式, eval 去除双引号获取表达式
        # generator = WeiboCookiesGenerator(website='weibo')
        generator = eval(cls + "(website='" + website + "')")
        # 调用父类.run()
        generator.run()
        # 输出提示
        print("Cookies 生成完成")
        # 关闭浏览器
        generator.close()
        # 周期休眠
        time.sleep(cycle)


if __name__ == '__main__':
    # 周期
    cycle = 3
    main(cycle)

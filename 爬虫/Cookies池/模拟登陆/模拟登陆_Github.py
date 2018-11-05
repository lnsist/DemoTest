"""
    模拟登陆 Github
date: 18-10-20 上午9:17
"""
import requests
from lxml import etree


class Login(object):
    """
        模拟登陆 Github
    """

    def __init__(self):
        """
            初始化
        """
        # 请求头
        self.headers = {
            "Referer": "https://github.com",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
            "Host": "github.com"
        }
        # 登陆路径
        self.login_url = "https://github.com/login"
        # 提交路径
        self.post_url = "https://gihub.com/seesion"
        # 个人信息路径
        self.logined_url = "https://github.com/settings/profile"
        # 会话 -- 自动处理Cookie
        self.session = requests.Session()

    def token(self):
        """
            获取表单提交参数
        :return: 表单参数
        """
        # 请求访问, 获取响应报文   verify 是否验证
        response = self.session.get(self.login_url, headers=self.headers, verify=False)
        # 加载响应报文
        selector = etree.HTML(response.text)
        # 解析数据, 获取表单参数
        token = selector.xpath("//form/input[2]/@value")[0]
        # 返回表单参数
        return token

    def login(self, email, password):
        """
            模拟登陆, 提交表单
        :param email: 账号
        :param password: 密码
        :return:
        """
        # 表单提交数据
        post_data = {
            "commit": "Sign in",
            "utf8": "✓",
            "authenticity_token": self.token(),
            "login": email,
            "password": password
        }
        # 请求访问, post_url 提交路径, post_data 提交参数, 请求头   verify 是否验证
        response = self.session.post(self.post_url, data=post_data, headers=self.headers, verify=False)
        # 如果返回状态码为200
        if response.status_code == 200:
            # 处理动态信息
            self.dynamics(response.text)

        # 请求访问, logined_url 个人信息路径, 请求头   verify 是否验证
        response = self.session.get(self.logined_url, headers=self.headers, verify=False)
        # 如果返回状态码为200
        if response.status_code == 200:
            # 处理个人信息
            self.profile(response.text)

    def dynamics(self, html):
        """
            提取动态信息
        :param html: 源码
        :return:
        """
        # 加载
        selector = etree.HTML(html)
        # 解析
        dynamics = selector.xpath("//div[contains(@class, 'news')]//div[contains(@class, 'alert')]")
        # 循环
        for item in dynamics:
            # 获取具体数据
            dynamic = " ".join(item.xpath(".//div[@class='title']//text()")).strip()
            # 输出提示
            print(dynamic)

    def profile(self, html):
        """
            处理个人信息
        :param html: 源码
        :return:
        """
        # 加载源码
        selector = etree.HTML(html)
        # 解析数据 -- 获取用户名
        name = selector.xpath("//input[@id='user_profile_name']/@value")[0]
        # 解析数据 -- 获取邮箱
        email = selector.xpath("//select[@id='user_profile_email']/option[@value!='']/text()")
        # 输出提示
        print(name, email)


if __name__ == '__main__':
    login = Login()
    login.login("lnsist@yeah.net", "Xx.992246086")

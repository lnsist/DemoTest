"""
    生成模块子类, 微博模拟登录获取Cookies
date: 18-10-20 下午10:51
"""
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from 爬虫.验证码.微博宫格验证码识别 import CrackWeiboSlide


class WeiboCookies(CrackWeiboSlide):
    """
        微博模拟登录获取Cookies
    """

    def __init__(self, username, password, browser):
        """
            初始化
        :param username: 用户名
        :param password: 密码
        :param browser: 浏览器
        """
        # 请求路径
        self.url = "https://passport.weibo.cn/signin/login?entry=mweibo&r=https://m.weibo.cn/"
        # 浏览器
        self.browser = browser
        # 浏览器等待器
        self.wait = WebDriverWait(self.browser, 20)
        # 用户名
        self.username = username
        # 密码
        self.password = password

    def password_error(self):
        """
            判断是否密码错误
        :return:
        """
        # 捕获异常
        try:
            # 5秒等待器, 等待指定内容控件出现 -- 出现此控件表示用户名或密码错误, 否则正常
            return WebDriverWait(self.browser, 5).until(
                EC.text_to_be_present_in_element((By.ID, 'errorMsg'), '用户名或密码错误'))
        except TimeoutException:
            # 正常
            return False

    def login_successfully(self):
        """
            判断是否登录成功
        :return:
        """
        # 捕获异常
        try:
            # 5秒等待器, 等待控件出现, 类选择器 -- 出现此控件表示登录成功
            return bool(
                WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'pannelwrap'))))
        except TimeoutException:
            # 登陆不成功
            return False

    def main(self):
        """
        破解入口
        :return:
        """
        # 打开浏览器, 设置账号密码, 并登录
        self.open()
        # 如果账号密码错误
        if self.password_error():
            # 返回账号密码错误信息
            return {
                'status': 2,
                'content': '用户名或密码错误'
            }
        # 如果不需要验证码直接登录成功
        if self.login_successfully():
            # 返回登陆成功信息, Cookies数据
            return {
                'status': 1,
                'content': self.browser.get_cookies()
            }
        # 可能会出现验证码
        # 设置浏览器
        # 获取验证码图片
        image = self.get_image("当前微博验证码图片.png")
        # 根据图片获取移动路径
        numbers = self.detect_image(image)
        # 模拟移动
        self.move(numbers)
        # 如果验证码通过, 并登录成功
        if self.login_successfully():
            # 返回登陆成功信息, Cookies数据
            return {
                'status': 1,
                'content': self.browser.get_cookies()
            }
        # 验证码不通过, 或者网络异常等问题
        else:
            # 返回登录失败信息
            return {
                'status': 3,
                'content': '登录失败'
            }

"""
    获取微博宫格验证码模板
    正常登陆账号不会出现验证码,
    需要频繁登陆获取账号存在安全风险的时候才会出现验证码,
    在请求访问的时候, 会判断是否出现验证码,
    没有出现验证码, 则重新请求访问,
    保存验证码图片过程中, 可能会出现重复图片, 需要多少循环访问保存图片,
    最后在多张图片中, 手动筛选出唯一的图片, 重新命名,
    命名方式为滑动宫格的顺序,
    如 Z字滑动 1 > 2 > 3 > 4 -- 1234.png
date: 18-10-11 下午4:04
"""
import os
import time
from io import BytesIO

from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 微博账号
USERNAME = "15285326066"
# 微博密码
PASSWORD = "iqr70760"


class TemplateWeiboSlide(object):
    """
        循环获取微博宫格验证码模板, 最后人工识别滑动顺序, 重命名
    """

    def __init__(self):
        """
            初始化
        """
        # 请求路径
        self.url = "https://passport.weibo.cn/signin/login"
        # 模拟浏览器 - google
        self.browser = webdriver.Chrome()
        # 浏览器等待器 超时时长20秒
        self.wait = WebDriverWait(self.browser, 20)
        # 账号
        self.username = USERNAME
        # 密码
        self.password = PASSWORD

    def __del__(self):
        """
            对象销毁
        :return:
        """
        # 关闭模拟浏览器
        self.browser.close()

    def open(self):
        """
            打开模拟浏览器, 访问路径 并设置账号 密码
        :return:
        """
        # 浏览器访问请求
        self.browser.get(self.url)
        # 浏览器等待器 等待控件出现 ID选择器 loginName -- 账号
        username = self.wait.until(EC.presence_of_element_located((By.ID, "loginName")))
        # 浏览器等待器 等待控件出现 ID选择器 loginPassword -- 密码
        password = self.wait.until(EC.presence_of_element_located((By.ID, "loginPassword")))
        # 浏览器等待器 等待控件可以点击 ID选择器 loginAction -- 提交按钮
        submit = self.wait.until(EC.element_to_be_clickable((By.ID, "loginAction")))
        # 输入账号
        username.send_keys(self.username)
        # 输入密码
        password.send_keys(self.password)
        # 点击提交
        submit.click()

    def get_position(self):
        """
            获取验证码控件位置坐标
        :return: 验证码控件位置坐标
        """
        # 捕获超时异常
        try:
            # 获取验证码控件 -- 等待器等待控件出现
            img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "patt-shadow")))
        except TimeoutException:
            # 输出提示
            print("未出现验证码")
            # 重新打开浏览器 并访问路径 -- 因为需要等账号出现登陆异常 才会出现验证码
            self.open()
        # 休眠
        time.sleep(2.2)
        # 获取验证码位置
        location = img.location
        # 获取验证码大小
        size = img.size
        # 获取控件 上下左右 坐标 -- 既四个角的坐标
        top, bottom, left, right = location["y"], location["y"] + size["height"], location["x"], location["x"] + size["width"]
        # 返回控件位置坐标
        return top, bottom, left, right

    def get_screenshot(self):
        """
            获取浏览器截图
        :return: 浏览器截图
        """
        # 获取浏览器截图
        screenshot = self.browser.get_screenshot_as_png()
        # 转换screenshot类型 -- image
        screenshot = Image.open(BytesIO(screenshot))
        # 返回浏览器截图
        return screenshot

    def get_image(self, name="captcha.png"):
        """
            获取验证码图片
        :param name: 验证码图片保存名字
        :return: 验证码图片
        """
        # 获取验证码位置坐标
        top, bottom, left, right = self.get_position()
        # 输出提示
        print("验证码位置:", top, bottom, left, right)
        # 获取浏览器截图
        screenshot = self.get_screenshot()
        # 在浏览器截图中, 根据验证码位置坐标, 截取验证码图片
        captcha = screenshot.crop((left, top, right, bottom))
        # 保存验证码图片
        captcha.save("./微博宫格验证码模板/" + name)
        # 返回验证码图片
        return captcha

    def main(self):
        """
           主接口 -- 批量获取验证码图片
        :return:
        """
        # 计数 -- 微博宫格验证码图片的列表数量
        count = len(os.listdir("./微博宫格验证码模板/"))
        # 死循环
        while True:
            # 打开浏览器
            self.open()
            # 保存验证码图片 -- 名字为次数
            self.get_image(str(count) + ".png")
            # 累计计数
            count += 1


if __name__ == '__main__':
    # 实例化
    slide = TemplateWeiboSlide()
    # 调用主接口
    slide.main()

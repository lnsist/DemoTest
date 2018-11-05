"""
    点触验证码 -- 看字在图片上按循序点击
    使用第三方平台验证服务
date: 18-10-9 下午8:16
"""
import time
from io import BytesIO

from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from 爬虫.验证码.第三方平台验证服务_超级鹰 import Chaojiying_Client as Chaojiying

# 邮箱
EMAIL = "lnsist@yeah.net"
# 密码
PASSWORD = ""
# 超级鹰_用户名
CHAOJIYING_USERNAME = "lnsist"
# 超级鹰_密码
CHAOJIYING_PASSWORD = ""
# 超级鹰_软件ID
CHAOJIYING_SOFT_ID = 893590
# 超级鹰_验证类型
CHAOJIYING_KIND = 9102


class CrackTouClick(object):
    """
        点触验证码识别
    """

    def __init__(self):
        # 网页路径
        self.url = "http://admin.touclick.com/login.html"
        # 模拟谷歌浏览器
        self.browser = webdriver.Chrome()
        # 浏览器超时时间 20 秒
        self.wait = WebDriverWait(self.browser, 20)
        # 邮箱
        self.email = EMAIL
        # 密码
        self.password = PASSWORD
        # 超级鹰实例
        self.chaojiying = Chaojiying(CHAOJIYING_USERNAME, CHAOJIYING_PASSWORD, CHAOJIYING_SOFT_ID)

    def open(self):
        """
            打开网页并输入
        :return:
        """
        # 访问网页
        self.browser.get(self.url)
        # 获取email控件
        email = self.wait.until(EC.presence_of_element_located((By.ID, "email")))
        # 获取password控件
        password = self.wait.until(EC.presence_of_element_located((By.ID, "password")))
        # 输入邮箱
        email.send_keys(self.email)
        # 输入密码
        password.send_keys(self.password)

    def get_touclick_button(self):
        """
            获取初始验证按钮
        :return: 初始验证按钮
        """
        # 获取初始验证按钮, 可点击
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "touclick-hod-wrap")))
        # 返回按钮
        return button

    def get_touclick_element(self):
        """
            获取验证码控件
        :return: 验证码控件
        """
        # 验证码控件
        element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "touclick-pub-content")))
        # 返回控件
        return element

    def get_position(self):
        """
            获取验证码控件位置坐标
        :return: 控件位置坐标
        """
        # 获取验证码控件
        element = self.get_touclick_element()
        # 休眠
        time.sleep(2)
        # 获取控件位置
        location = element.location
        # 获取控件大小
        size = element.size
        # 计算返回 控件上下左右 坐标
        top, bottom, left, right = location["y"], location["y"] + size["height"], location["x"], location["x"] + size["width"]
        # 返回坐标
        return top, bottom, left, right

    def get_screenshot(self):
        """
            获取浏览器截图图片
        :return: 截图图片
        """
        # 获取浏览器截图流
        screenshot = self.browser.get_screenshot_as_png()
        # 将截图流转为图片
        screenshot = Image.open(BytesIO(screenshot))
        # 返回截图图片
        return screenshot

    def get_touclick_iamge(self, name="captcha.png"):
        """
            根据验证码控件位置, 具体截图验证码图片
        :param name: 验证码图片名称
        :return: 验证码图片
        """
        # 获取验证码控件位置
        top, bottom, left, right = self.get_position()
        # 输出提示
        print("验证码控件位置:", top, bottom, left, right)
        # 获取浏览器截图
        screenshot = self.get_screenshot()
        # 从截图中具体截取验证码图片
        captcha = screenshot.crop((left, top, right, bottom))
        # 保存图片
        captcha.save(name)
        # 返回验证码图片
        return captcha

    def get_points(self, captcha_result):
        """
            解析服务器响应报文
            {"err_no": 0,                               # 是否报错
            "err_str": "OK",                            # 错误信息
            "pic_id": "6002001380949200001",            # 图片id
            "pic_str": "132,127|56,77",                 # 图片坐标, 顺序点击
            "md5": "1f8e1d4bef8b11484cb1f1f3429986Sb"   # md5 加密}
        :param captcha_result: 服务器响应报文 - json格式
        :return: 图片坐标解析结果
        """
        # 获取图片坐标并分割
        groups = captcha_result.get("pic_str").split("|")
        # 列表推导式 - 将图片坐标","分割后封装列表中
        locations = [[int(number) for number in group.split(",")] for group in groups]
        # 返回图片坐标解析结果
        return locations

    def touch_click_words(self, locations):
        """
            根据图片坐标循环点击验证码
        :param locations:
        :return:
        """
        # 循环图片坐标
        for location in locations:
            # 输入当前坐标
            print(locations)
            # 模拟在 浏览器中的 验证码控件中 坐标点击.perform执行
            ActionChains(self.browser).move_to_element_with_offset(self.get_touclick_element(), location[0], locations[1]).click().perform()
            # 休眠
            time.sleep(1)

    def main(self):
        """
            执行验证码识别
        :return:
        """
        # 打开网页并输入信息
        self.open()
        # 获取初始验证按钮
        button = self.get_touclick_button()
        # 点击
        button.click()
        # 获取验证码图片
        image = self.get_touclick_iamge("点触验证码.png")
        # 设置字节组
        bytes_array = BytesIO()
        # 将图片转换为字节流
        image.save(bytes_array, format="png")
        # 使用第三方平台验证服务, 访问服务器获取响应
        result = self.chaojiying.PostPic(bytes_array.getvalue(), CHAOJIYING_KIND)
        # 根据服务器响应, 获取图片坐标
        locations = self.get_points(result)
        # 根据图片坐标, 模拟点击
        self.touch_click_words(locations)


if __name__ == '__main__':
    # 创建实例
    ctc = CrackTouClick()
    # 执行验证码识别
    ctc.main()

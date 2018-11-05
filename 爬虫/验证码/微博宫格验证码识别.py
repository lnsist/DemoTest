"""
    微博宫格验证码识别
    打开模拟浏览器, 访问路径,
    获取当前验证码图片 和 模板图片 进行对比,
    获取相同的图片后, 对模板图片名字进行分割, 获取到滑动顺序,
    获取浏览器上宫格的控件列表,
    根据滑动顺序, 进行模拟滑动
date: 18-10-11 下午4:46
"""
import os
import time
from io import BytesIO

from PIL import Image
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# 微博账号
USERNAME = "15285326066"
# 微博密码
PASSWORD = "iqr70760"


class CrackWeiboSlide(object):
    """
        微博宫格验证码识别
    """

    def __init__(self):
        """
            初始化
        """
        # 请求路径
        self.url = "https://passport.weibo.cn/signin/login"
        # 模拟浏览器 -- google
        self.browser = webdriver.Chrome()
        # 浏览器等待器 超时时长20秒
        self.wait = WebDriverWait(self.browser, 20)
        # 账号
        self.username = USERNAME
        # 密码
        self.password = PASSWORD

    def open(self):
        """
            打开网页输入用户名密码并点击
        :return: None
        """
        # 删除当前Cookies
        self.browser.delete_all_cookies()
        # 请求访问
        self.browser.get(self.url)
        # 等待器, 等待控件出现, ID选择器 -- 账号输入框
        username = self.wait.until(EC.presence_of_element_located((By.ID, 'loginName')))
        # 等待器, 等待控件出现, ID选择器 -- 密码输入框
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'loginPassword')))
        # 等待器, 等待控件可点击, ID选择器 -- 登陆按钮
        submit = self.wait.until(EC.element_to_be_clickable((By.ID, 'loginAction')))
        # 设置账号
        username.send_keys(self.username)
        # 设置密码
        password.send_keys(self.password)
        # 点击登陆
        submit.click()

    def get_position(self):
        """
            获取验证码控件位置坐标
        :return: 验证码控件位置坐标
        """
        # 捕获超时异常
        try:
            # 验证码控件
            img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "patt-shadow")))
        except TimeoutException:
            # 输出提示
            print("没有验证码")
            # 重新访问
            self.open()
        # 休眠
        time.sleep(2.2)
        # 获取验证码控件位置
        location = img.location
        # 获取验证码控件大小
        size = img.size
        # 获取验证码控件, 上下左右 坐标
        top, bottom, left, right = location["y"], location["y"] + size["height"], location["x"], location["x"] + size["width"]
        # 返回验证码控件位置坐标
        return top, bottom, left, right

    def get_screenshot(self):
        """
            获取浏览器截图图片
        :return: 浏览器截图图片
        """
        # 获取模拟浏览器截图
        screenshot = self.browser.get_screenshot_as_png()
        # 模拟浏览器截图 转 image
        screenshot = Image.open(BytesIO(screenshot))
        # 返回浏览器截图图片
        return screenshot

    def get_image(self, name="captcha.png"):
        """
            根据验证码位置坐标 在浏览器截图图片中截取验证码图片
        :return: 验证码图片
        """
        # 验证码上下左右位置
        top, bottom, left, right = self.get_position()
        # 输出提示
        print("验证码位置:", top, bottom, left, right)
        # 获取浏览器截图
        screenshot = self.get_screenshot()
        # 从浏览器截图中, 根据验证码位置截取图片
        captcha = screenshot.crop((left, top, right, bottom))
        # 保存验证码图片
        captcha.save(name)
        # 返回验证码图片
        return captcha

    def detect_image(self, image):
        """
            根据当前验证码图片, 循环匹配模板相同的图片, 返回滑动顺序
        :param image: 当前验证码图片
        :return: 滑动顺序
        """
        # 循环模板目录, 获取每一张模板图片
        for template_name in os.listdir("/home/lnsist/AllProjects/PycharmProjecs/DemoTest/爬虫/验证码/微博宫格验证码模板/"):
            # 输出提示
            print("正在匹配 --", template_name)
            # 打开模板图片
            template = Image.open("/home/lnsist/AllProjects/PycharmProjecs/DemoTest/爬虫/验证码/微博宫格验证码模板/" + template_name)
            # 循环像素判断 当前验证码图片 和 模板图片 一致
            if self.same_image(image, template):
                # 切割模板名称, 获取滑动顺序
                numbers = [int(num) for num in template_name.split(".")[0]]
                # 输出提示
                print("滑动顺序:", numbers)
                # 返回滑动顺序
                return numbers

    def same_image(self, image, template):
        """
            识别相似验证码
        :param image: 验证码图片
        :param template: 模板图片
        :return: 是否相似
        """
        # 相似度阀值
        threshold = 0.99
        # 计数 -- 相似的像素点
        count = 0
        # 循环 验证码图片 宽度
        for x in range(image.width):
            # 循环 验证码图片 高度
            for y in range(image.height):
                # 验证码图片 和 模板图片 的每个像素对比, 是否一致
                if self.is_pixel_equal(image, template, x, y):
                    # 相似点则+1
                    count += 1
        # 相似点 / (验证码图片的宽 * 验证码图片的高)
        result = float(count) / (image.width * image.height)
        # 如果大于相似阀值
        if result > threshold:
            # 输入提示
            print("成功匹配")
            # 返回真相似
            return True
        # 返回假相似
        return False

    @staticmethod
    def is_pixel_equal(image, template, x, y):
        """
            判断当前像素点2张图片是否一致
        :param image: 验证码图片
        :param template: 模板图片
        :param x: x 坐标
        :param y: y 坐标
        :return: 是否一致
        """
        # 获取验证码图片 [x,y] 坐标像素点
        pixel1 = image.load()[x, y]
        # 获取模板图片 [x,y] 坐标像素点
        pixel2 = template.load()[x, y]
        # 阀值
        threshold = 20
        # 2个像素点的 三维 相减 < 阀值 就是真一致
        if (abs(pixel1[0] - pixel2[0]) < threshold and
                abs(pixel1[1] - pixel2[1]) < threshold and
                abs(pixel1[2] - pixel2[2]) < threshold):
            # 真一致
            return True
        # 假一致
        return False

    def move(self, numbers):
        """
            模拟滑动
        :param numbers : 滑动顺序
        :return:
        """
        # 获取宫格验证码的4个滑块列表
        circles = self.browser.find_elements_by_css_selector(".patt-wrap .patt-circ")
        # x轴移动偏移量, y轴移动偏移量
        dx = dy = 0
        # 循环4次
        for index in range(4):
            # 获取当前滑动顺序的滑块, 滑动顺序是1到4, 控件是0到3
            circle = circles[numbers[index] - 1]
            # 如果是第一个滑块
            if index == 0:
                # 点击并按住滑块中心
                ActionChains(self.browser) \
                    .move_to_element_with_offset(circle, circle.size["width"] / 2, circle.size["height"] / 2) \
                    .click_and_hold().perform()
            # 否则
            else:
                # 小幅移动次数
                times = 30
                # 循环移动次数
                for i in range(times):
                    # 模拟滑动
                    ActionChains(self.browser).move_by_offset(dx / times, dy / times).perform()
                    # 休眠
                    time.sleep(1 / times)
            # 如果是最后一次滑动
            if index == 3:
                # 滑动结束, 松开鼠标
                ActionChains(self.browser).release().perform()
            # 否则
            else:
                # 计算下次移动偏移量
                dx = circles[numbers[index + 1] - 1].location["x"] - circle.location["x"]
                dy = circles[numbers[index + 1] - 1].location["y"] - circle.location["y"]

    def main(self):
        """
            主接口 - 识别宫格验证码步骤
        :return:
        """
        # 打开浏览器
        self.open()
        # 获取当前验证码图片
        image = self.get_image("当前微博验证码图片.png")
        # 根据当前验证码图片, 循环匹配模板图片, 获取滑动顺序
        numbers = self.detect_image(image)
        # 根据滑动顺序, 模拟滑动
        self.move(numbers)


if __name__ == '__main__':
    # 实例化
    slide = CrackWeiboSlide()
    # 调用主接口
    slide.main()

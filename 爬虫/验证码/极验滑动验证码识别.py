"""

date: 18-10-8 下午6:38
"""
import time
from io import BytesIO

from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 登陆邮箱
EMAIL = "lnsist@yeah.net"
# 登陆密码
PASSWORD = "Xx123456"
# 图片边缘
BORDER = 6


# 极验验证码识别
class CrackGeetest(object):
    # 初始化
    def __init__(self):
        # 网址
        self.url = "https://account.geetest.com/login"
        # 模拟浏览器
        self.browser = webdriver.Chrome()
        # 浏览器超时时间 20秒
        self.wait = WebDriverWait(self.browser, 20)
        # 登陆邮箱
        self.email = EMAIL
        # 登陆密码
        self.password = PASSWORD

    def __del__(self):
        # 关闭浏览器
        self.browser.close()

    def open(self):
        """
            打开网页输入用户名密码
        :return: None
        """
        # 访问网页
        self.browser.get(self.url)
        # 获取 邮箱输入框
        email = self.wait.until(EC.presence_of_element_located((By.ID, 'email')))
        # 获取 密码输入框
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'password')))
        # 输入邮箱
        email.send_keys(self.email)
        # 输入密码
        password.send_keys(self.password)

    def get_geetest_buton(self):
        """
            获取初始验证按钮
        :return: 返回初始验证按钮
        """
        # 根据类名, 获取初始验证按钮
        button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "geetest_radar_tip")))
        # 返回初始验证按钮
        return button

    def get_position(self):
        """
            识别缺口位置
            首先获取前后 2 张图片做对比, 二者不一致的地方就是缺口
            利用模拟浏览器的截图将完好的图片截取下来
        :return: 返回图片上下左右坐标
        """
        # 根据类名, 获取滑动验证码图片
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "geetest_canvas_img")))
        # 休眠 2 秒
        time.sleep(2)
        # 获取图片位置
        location = img.location
        # 获取图片大小
        size = img.size
        # 通过图片的位置 和 图片的大小, 获取图片的 上 下 左 右 坐标
        top, bottom, left, right = location["y"], location["y"] + size["height"], location["x"], location["x"] + size["width"]
        # 返回图片上下左右坐标
        return top, bottom, left, right

    def get_screenshot(self):
        """
            获取网页截图
        :return: 截图对象
        """
        # 获取当前图片
        screenshot = self.browser.get_screenshot_as_png()
        # 打开图片
        screenshot = Image.open(BytesIO(screenshot))
        # 返回图片
        return screenshot

    def get_geetest_image(self, name="captcha.png"):
        """
            根据图片的上下左右坐标 截图完好图片
        :param name: 图片
        :return: 返回截取到的图片
        """
        # 获取图片上下左右坐标
        top, bottom, left, right = self.get_position()
        # 输出坐标
        print("验证码位置:", top, bottom, left, right)
        # 获取整个浏览器屏幕
        screenshot = self.get_screenshot()
        # 根据 左上右下 坐标截取图片
        captcha = screenshot.crop((left, top, right, bottom))
        # 保存图片
        captcha.save(name)
        # 返回截取到的图片
        return captcha

    def get_slider(self):
        """
            获取滑块
        :return: 返回滑块按钮
        """
        # 根据类名获取滑块按钮
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "geetest_slider_button")))
        # 返回滑块按钮
        return slider

    def is_pixel_equal(self, image1, image2, x, y):
        """
            判断 2 张图片的像素是否相同
        :param image1: 图片1
        :param image2: 图片2
        :param x: x 坐标
        :param y: y 坐标
        :return: 2 张图片的像素是否相同
        """
        # 获取 图片1 的 (x,y) 的像素点
        pixel1 = image1.load()[x, y]
        # 获取 图片2 的 (x,y) 的像素点
        pixel2 = image2.load()[x, y]
        # 阀值
        threshold = 120
        # 2张图片像素点的 3围 绝对值 对比 阀值
        if (abs(pixel1[0] - pixel2[0]) < threshold
                and abs(pixel1[1] - pixel2[1]) < threshold
                and abs(pixel1[2] - pixel2[2]) < threshold):
            # 相同
            return True
        else:
            # 不相同
            return False

    def get_gap(self, image1, image2):
        """
            获取缺口坐标
        :param image1: 图片1 完好图片
        :param image2: 图片2 缺口图片
        :return: 偏移量 --  缺口x坐标
        """
        # 起始x坐标
        left = 10
        # 循环图片x坐标, 从left开始
        for i in range(left, image1.size[0]):
            # 循环图片y坐标
            for j in range(image1.size[1]):
                # 将图片的 (x,y) 坐标传参, 对比图片, 判断当前像素点是否缺口
                if not self.is_pixel_equal(image1, image2, i, j):
                    # 获取当前x坐标
                    left = i
                    # 返回当前x坐标, 既缺口x坐标
                    return left
        # 返回当前坐标, 默认起始x坐标 60
        return left

    def get_track(self, distance):
        """
            根据偏移量获取移动轨迹 -- 使用物理学的加速度公式计算
        :param distance: 偏移量 -- 移动的总距离
        :return: 移动轨迹
        """
        # 移动轨迹
        track = []
        # 当前位置
        current = 0
        # 减速阀值 -- 前4/5的距离是加速度, 后1/5的距离是减速度
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.2
        # 当前速度
        v = 0

        # 如果当前位置 小于 偏移量
        while current < distance:
            # 如果当前位置 小于 减速阀值
            if current < mid:
                # 加速度
                a = 2
            else:
                # 减速度
                a = -3
            # 初始速度
            v0 = v
            # 当前速度 = 初始速度 * 加速度 * 时间
            v = v0 + a * t
            # 移动距离 = 初始速度 * 时间 + 1/2的 加速度 * 时间的平方
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位置 += 移动距离
            current += move
            # 出去小数添加至 移动轨迹
            track.append(round(move))
        # 返回移动轨迹
        return track

    def move_to_gap(self, slider, tracks):
        """
            根据移动轨迹, 滑动滑块
        :param slider:  滑块
        :param tracks:  移动轨迹
        :return:
        """
        # 获取当前 模拟浏览器 中的滑块slider 点击并按住. perform执行
        ActionChains(self.browser).click_and_hold(slider).perform()
        # 循环移动轨迹, x移动
        for x in tracks:
            # 获取当前 模拟浏览器 移动偏移量 x移动, y不变. perform执行
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
        # 休眠0.5秒
        time.sleep(0.5)
        # 获取当前 模拟浏览器 松开鼠标. perform执行
        ActionChains(self.browser).release().perform()

    def login(self):
        """
            登录
        :return: None
        """
        # 登陆 按钮
        submit = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'login-btn')))
        # 点击按钮
        submit.click()
        # 休眠
        time.sleep(10)
        # 输入提示
        print('登录成功')

    def main(self):
        """
            主函数
        :return:
        """
        # 输入用户名密码
        self.open()
        # 获取 初始验证按钮
        button = self.get_geetest_buton()
        # 初始验证按钮点击
        button.click()
        # 获取完好图片
        perfection_iamge = self.get_geetest_image("完好图片.png")
        # 获取滑块
        slider = self.get_slider()
        # 点击滑块, 出现缺口图片
        slider.click()
        # 获取缺口图片
        gap_iamge = self.get_geetest_image("缺口图片.png")
        # 获取缺口位置 -- 偏移量
        distance = self.get_gap(perfection_iamge, gap_iamge)
        # 去除边界
        distance -= BORDER
        # 获取移动轨迹
        tracks = self.get_track(distance)
        # 根据移动轨迹, 滑动滑块
        self.move_to_gap(slider, tracks)
        # 获取验证成功
        success = self.wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "geetest_success_radar_tip_content"), "验证成功"))
        # 输出
        print(success)

        # 失败后重试
        if not success:
            # 重新验证
            self.main()
        else:
            # 成功验证 点击登陆
            self.login()


def main():
    # 创建实例对象
    cg = CrackGeetest()
    # 执行验证并登陆
    cg.main()


if __name__ == '__main__':
    main()

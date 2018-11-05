"""
    使用Appium爬取手机APP
个人感觉, 是先通过Appium录制操作, 生成代码, 然后在脚本使用, 达到真实人工操作,
然后爬取数据, 存储数据, 其他控件手机框架, 无法爬取的一些数据, Appium也可以爬取,
因为Appium是模拟人工操作, 显示出来的数据, 都可以爬取,
date: 18-10-25 下午5:09
"""
import re
import time

import pymongo
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# 手机操作系统
PLATFORM_NAME = "Android"
# 手机型号
DEVICE_NAME = "SM_G9350"
# APP包名
APP_PACKAGE = "com.tencent.mm"
# APP入口
APP_ACTIVITY = ".ui.LauncherUI"
# Appium服务路径
DRIVER_SERVER = "http://localhost:4723/wd/hub"
# 超时时间
TIMEOUT = 300
# 数据库路径
MONGO_URL = "localhost"
# 数据库 -- 名称
MONGO_DB = "moments"
# 数据库 -- 连接
MONGO_COLLECTION = "moments"
# 滑动开始X坐标
FLICK_START_X = 300
# 滑动开始Y坐标
FLICK_START_Y = 300
# 滑动距离
FLICK_DISTANCE = 700


class Moments(object):
    """
        爬取微信朋友圈
    """

    def __init__(self):
        """
            初始化
        """
        # 驱动配置
        self.desired_caps = {
            "platformName": PLATFORM_NAME,
            "deviceName": DEVICE_NAME,
            "appPackage": APP_PACKAGE,
            "appActivity": APP_ACTIVITY
        }
        # 获取Appium驱动
        self.driver = webdriver.Remote(DRIVER_SERVER, self.desired_caps)
        # 等待器
        self.wait = WebDriverWait(self.driver, TIMEOUT)
        # 数据库客户端
        self.client = pymongo.MongoClient(MONGO_URL)
        # 获取数据库
        self.db = self.client[MONGO_DB]
        # 获取数据库连接
        self.collection = self.db[MONGO_COLLECTION]

    def load_finish(self, element_id, is_located):
        """
            根据判断加载元素ID出现或消失, 确定是否加载完毕
        :param element_id: 加载元素id
        :param is_located: 判断元素是出现, 还是消失, True 出现, False 消失
        :return:
        """
        # 重新实例化等待器 -- 1 秒等待
        wait = WebDriverWait(self.driver, 0)
        # 死循环
        while True:
            # 输出提示
            print("等待加载完毕")
            # 捕获异常
            try:
                # 休眠
                time.sleep(1)
                # 一直获取此元素, 根据 is_located 决定是出现元素为加载完毕, 还是消失元素为加载完毕
                wait.until(EC.presence_of_element_located((By.ID, element_id)))
                # 如果需要确定 element_id 是出现
                if is_located:
                    # 输出提示
                    print("元素已出现, 加载已完毕, 跳出循环, 继续执行")
                    # 跳出循环
                    break
            # 超时异常
            except TimeoutException:
                # 如果需要确定 element_id 是消失
                if not is_located:
                    # 输出提示
                    print("元素已消失, 加载已完毕, 跳出循环, 继续执行")
                    # 跳出循环
                    break

        # 休眠 -- 退出方法前
        time.sleep(1)

    def login(self):
        """
            登陆微信
        :return:
        """
        # 输出提示
        print("文件权限, 允许")
        # 文件权限 - - 总是允许
        el1 = self.wait.until(EC.presence_of_element_located((By.ID, "com.android.packageinstaller:id/permission_allow_button")))
        el1.click()

        # 输出提示
        print("通话权限, 允许")
        # 通话权限 - - 总是允许
        el2 = self.wait.until(EC.presence_of_element_located((By.ID, "com.android.packageinstaller:id/permission_allow_button")))
        el2.click()

        # 休眠
        time.sleep(1)
        # 输出提示
        print("点击登录, 坐标点击")
        # 点击登陆 -- 坐标点击
        TouchAction(self.driver).tap(x=238, y=1776).perform()

        # 输出提示
        print("点击手机号码, 并输入手机")
        # 点击手机号码, 并输入手机
        el3 = self.wait.until(EC.presence_of_element_located((By.ID, "com.tencent.mm:id/ji")))
        el3.click()
        el3.send_keys("13318766890")

        # 输出提示
        print("点击下一步")
        # 点击下一步
        el4 = self.wait.until(EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/ast")))
        el4.click()

        # 输出提示
        print("点击密码, 并输入密码")
        # 密码
        el5 = self.wait.until(EC.presence_of_element_located((By.ID, "com.tencent.mm:id/ji")))
        el5.click()
        el5.send_keys("Xx.992246086")

        # 输出提示
        print("点击登录")
        # 登陆
        el6 = self.wait.until(EC.element_to_be_clickable((By.ID, "com.tencent.mm:id/ast")))
        el6.click()

        # 输出提示
        print("匹配通讯录")
        # 不匹配通讯录
        # el7 = self.wait.until(EC.presence_of_element_located((By.ID, "com.tencent.mm:id/au9")))
        # 匹配通讯录
        el7 = self.wait.until(EC.presence_of_element_located((By.ID, "com.tencent.mm:id/au_")))
        el7.click()

    def enter(self):
        """
            进入朋友圈
        :return:
        """
        # 元素消失, 加载完毕
        self.load_finish("com.tencent.mm:id/a2r", False)

        # 输出提示
        print("点击发现 -- 坐标点击")
        # 点击发现 -- 坐标点击
        TouchAction(self.driver).tap(x=670, y=1829).perform()

        # 输出提示
        print("进入朋友圈")
        # 朋友圈
        el1 = self.wait.until(EC.presence_of_element_located((By.ID, "com.tencent.mm:id/kl")))
        el1.click()

    @staticmethod
    def processor_date(date):
        """
            处理时间 -- 获取具体日期
        :param date: 时间
        :return: 具体日期
        """
        # 格式化后的日期
        datetime = ""

        # xx 分钟前
        if re.match("\d+分钟前", date):
            # 获取具体分钟数
            miute = re.match("(\d+)", date).group()
            # 格式 yyyy-mm-dd H:M:S   时间  当前时间秒数 减去 (分钟数 * 60秒)秒
            datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() - float(miute) * 60))

        # xx 小时前
        if re.match("\d+小时前", date):
            # 获取具体小时数
            hour = re.match("(\d+)", date).group()
            # 格式 yyyy-mm-dd H:M:S   时间  当前时间秒数 减去 (小时数 * 60分 * 60秒)秒
            datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() - float(hour) * 60 * 60))

        # 昨天
        if re.match("昨天", date):
            # 格式 yyyy-mm-dd H:M:S   时间  当前时间秒数 减去 (24小时 * 60分 * 60秒)秒
            datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() - 24 * 60 * 60))

        # xx 天前
        if re.match("\d+天前", date):
            # 获取具体天数
            day = re.match("(\d+)", date).group()
            # 格式 yyyy-mm-dd H:M:S   时间  当前时间秒数 减去 天数 * 24小时 * 60分 * 60秒
            datetime = time.strftime("%Y-%m-%d", time.localtime(time.time() - float(day) * 24 * 60 * 60))

        # 返回具体日期
        return datetime

    def crawl(self):
        """
            滑动屏幕刷新朋友圈
        :return:
        """
        # 元素出现, 加载完毕
        self.load_finish("com.tencent.mm:id/e6t", True)
        # 死循环
        while True:
            # 输出提示
            print("循环滑动屏幕, 获取动态")
            # 上滑屏幕 -- 从(X, Y + D)开始, 滑到(X, Y) 滑动了D的距离
            self.driver.swipe(FLICK_START_X, FLICK_START_Y + FLICK_DISTANCE, FLICK_START_X, FLICK_START_Y)

            # 每条动态
            items = self.wait.until(EC.presence_of_all_elements_located((By.ID, "com.tencent.mm:id/e2p")))

            # 循环获取
            for item in items:
                # 捕获异常
                try:
                    # 捕获异常
                    try:
                        # 如果是朋友圈封面, 则不获取信息
                        if item.find_element_by_id("com.tencent.mm:id/e3i"):
                            # 输出提示
                            print("当前获取的元素是封面, 跳过此次循环")
                            # 跳过此次获取信息
                            continue
                    # 标签不存在
                    except Exception as e:
                        # 输出异常提示
                        print(e)
                    # 昵称
                    nickname = item.find_element_by_id("com.tencent.mm:id/azl").get_attribute("text")
                    # 正文
                    content = item.find_element_by_id("com.tencent.mm:id/e6x").get_attribute("text")
                    # 日期
                    date = item.find_element_by_id("com.tencent.mm:id/e25").get_attribute("text")
                    # 处理日期
                    date = self.processor_date(date.strip())
                    # 由于数据是动态的, 页面加载不到的元素, 就不会出现, 需要非空判断
                    if not nickname.strip() or not content.strip():
                        # 输出提示
                        print("昵称为空 或 正文为空, 跳过此次循环")
                        # 只要有一个为空则跳过此次循环
                        continue

                    # 输出提示
                    print("获取到的数据: ", nickname, content, date)
                    # 封装
                    data = {
                        "nickname": nickname,
                        "content": content,
                        "date": date
                    }

                    # 保存数据库 -- 去重, 先根据(昵称, 正文)查询数据, 存在则更新, 不存在则插入
                    # 操作的数据 {"set": date}
                    # True 控制 存在则更新, 不存在则插入
                    self.collection.update({"nickname": nickname, "content": content}, {"set": data}, True)
                # 元素不存在
                except NoSuchElementException:
                    pass
            # 休眠
            time.sleep(1)

    def main(self):
        """
            主入口
        :return:
        """
        # 登陆
        self.login()
        # 进入朋友圈
        self.enter()
        # 循环滑屏 -- 爬取信息
        self.crawl()


if __name__ == '__main__':
    Moments().main()

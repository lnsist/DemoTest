"""
    ADSL拨号模块 -- 定时拨号 或 非定时拨号, 更新数据库
    非定时拨号: 通过web服务向主机传递一个拨号请求, 主机才会去拨号,
                但是拨号过程主机web服务是无法访问的, 等待主机拨号成功才能获取代理
    定时拨号: 主机运行定时拨号脚本, 自动拨号换IP更新数据库,
                程序只需要访问数据库就可以获取到可用的代理
date: 18-10-16 上午9:48
"""
import re
import subprocess
import time
import requests
from requests.exceptions import ConnectionError, ReadTimeout
from 爬虫.代理.ADSL代理池.ADSL代理池_存储模块 import RedisClient

# 拨号网卡
ADSL_IFNAME = "ppp0"
# 测试URL
TEST_URL = "http://www.baidu.com"
# 测试超时时间
TEST_TIMEOUT = 20
# 拨号周期
ADSL_CYCLE = 100
# 拨号出错重试周期
ADSL_ERROR_CYCLE = 5
# ADSL命令
ADSL_BASH = "adsl-stop:adsl-start"
# 代理运行端口
PROXY_PORT = 8888
# 客户端唯一标识
CLIENT_NAME = "adsl1"


class Sender(object):
    """
        ADSL拨号模块
    """

    def __init__(self):
        """
            初始化
        """
        # Redis数据库连接
        self.redis = RedisClient()

    @staticmethod
    def get_ip(ifname=ADSL_IFNAME):
        """
            获取本机ip
        :param ifname: 网卡名称
        :return: 本机IP
        """
        # subprocess系统交互, 开启新线程, 执行cmd命令, 返回一个元组(执行状态, 执行结果)
        status, output = subprocess.getstatusoutput('ifconfig')
        # 执行状态 成功
        if status == 0:
            # 创建 正则表达式匹配获取IP 模板
            pattern = re.compile(ifname + ".*?inet.*?(\d+.\d+.\d+.\d+).*?netmask", re.S)
            # 在执行结果中, 匹配出IP
            result = re.search(pattern, output)
            # 匹配IP成功
            if result:
                # 获取第二组真正本机的IP, 第一组IP是回路
                ip = result.group(1)
                # 返回IP
                return ip

    @staticmethod
    def test_proxy(proxy):
        """
            测试代理
        :param proxy: 代理
        :return: 测试结果
        """
        # 捕获异常
        try:
            # 设计代理, 请求访问, 获取响应报文
            response = requests.get(TEST_URL, proxies={"http": "http://" + proxy, "https": "https://" + proxy}, timeout=TEST_TIMEOUT)
            # 响应状态码 200 为成功访问
            if response.status_codes == 200:
                # 返回真 -- 代理可用
                return True
        except (ConnectionError, ReadTimeout):
            # 连接错误, 超时错误, 异常
            # 返回假 -- 代理不可用
            return False

    def remove_proxy(self):
        """
            删除代理
        :return:
        """
        # 删除当前主机代理
        self.redis.remove_proxy(CLIENT_NAME)
        # 输出提示
        print("删除代理 -- 成功")

    def set_porxy(self, proxy):
        """
            保存代理
        :param proxy: 代理
        :return:
        """
        # 数据库保存数据成功
        if self.redis.set(CLIENT_NAME, proxy):
            # 输出提示
            print("保存代理 -- 成功")

    def adsl(self):
        """
            拨号主进程
        :return:
        """
        # 死循环
        while True:
            # 输出提示
            print("ADSL拨号开始, 移除数据库代理, 拨号中...")
            # 移除当成主机数据库代理
            self.remove_proxy()
            # subprocess系统交互, 开启新线程, 执行cmd命令, 返回一个元组(执行状态, 执行结果)
            status, output = subprocess.getstatusoutput(ADSL_BASH)
            # 执行结果, 成功
            if status == 0:
                # 输出提示
                print("ADSL拨号 -- 成功")
                # 拨号成功, 获取当前IP
                ip = self.get_ip()
                # 获取成功
                if ip:
                    # 输出提示
                    print("当前IP:", ip)
                    # 输出提示
                    print("测试代理...")
                    # 代理文本格式化
                    proxy = "{ip}:{proxy}".format(ip=ip, proxy=PROXY_PORT)
                    # 测试代理成功
                    if self.test_proxy(proxy):
                        # 输出提示
                        print("测试代理 -- 成功")
                        # 保存代理到数据库
                        self.set_porxy(proxy)
                        # 输出提示
                        print("保存代理 -- 成功")
                        # 休眠
                        time.sleep(ADSL_CYCLE)
                    else:
                        # 测试代理 -- 失败
                        # 输出提示
                        print("测试代理 -- 失败")
                else:
                    # 获取IP -- 失败, 重新拨号
                    # 输出提示
                    print("获取IP -- 失败, 重新拨号")
                    # 休眠
                    time.sleep(ADSL_ERROR_CYCLE)
            else:
                # ADSL拨号 -- 失败, 重新拨号
                # 输出提示
                print("ADSL拨号 -- 失败, 重新拨号")
                # 休眠
                time.sleep(ADSL_ERROR_CYCLE)

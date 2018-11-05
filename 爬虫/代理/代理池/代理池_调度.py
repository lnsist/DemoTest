"""
    调度模块, 调度代理池的4个基本模块, 以多任务的方式运行
date: 18-10-14 上午10:09
"""
import time
from multiprocessing import Process

from 爬虫.代理.代理池.代理池_检测模块 import Tester
from 爬虫.代理.代理池.代理池_获取模块 import Getter
import 爬虫.代理.代理池.代理池_接口模块 as Apier

# 检测模块周期
TESTER_CYCLE = 20
# 获取模块周期
GETTER_CYCLE = 20
# 检测模块开关
TESTER_ENABLED = True
# 获取模块开关
GETTER_ENABLED = False
# 接口模块开关
API_ENABLED = True


class Scheduler(object):
    """
        调度模块, 整理调度代理池的4个基本模块
    """

    def __init__(self, test_url, min_score):
        """
            初始化
        :param test_url: 测试路径
        :param min_score:  最低分
        """
        self.test_url = test_url
        self.min_score = min_score

    def schedule_tester(self, cycle=TESTER_CYCLE):
        """
            检测模块的周期调度
        :param cycle: 周期
        :return:
        """
        # 创建检测模块实例
        tester = Tester()
        # 死循环
        while True:
            # 输出提示
            print("检测模块开始运行")
            # 运行检测模块 -- 检测最小值100到最大值100的数据
            tester.run(test_url=self.test_url, min_score=self.min_score)
            # 周期休眠
            time.sleep(cycle)

    @staticmethod
    def schedule_getter(cycle=GETTER_CYCLE):
        """
            获取模块的周期调度
        :param cycle: 周期
        :return:
        """
        # 创建获取模块实例
        getter = Getter()
        # 死循环
        while True:
            # 输出提示
            print("获取模块开始运行")
            # 运行获取模块
            getter.run()
            # 周期休眠
            time.sleep(cycle)

    @staticmethod
    def schedule_api():
        """
            接口模块的调度
        :return:
        """
        # 接口模块开启服务
        Apier.start_flask()

    def run(self):
        """
            调度代理池, 整合所有功能
        :return:
        """
        # 输出提示
        print("代理池开始运行")
        # 检测模块开启
        if TESTER_ENABLED:
            # 创建进程 -- 检测模块, 最小分数 100
            tester_process = Process(target=self.schedule_tester)
            # 进程启动
            tester_process.start()
        # 获取模块开启
        if GETTER_ENABLED:
            # 创建进程 -- 获取模块
            getter_process = Process(target=self.schedule_getter)
            # 进程启动
            getter_process.start()
        # 接口模块开启
        if API_ENABLED:
            # 创建进程 -- 接口模块
            api_process = Process(target=self.schedule_api)
            # 进程启动
            api_process.start()


if __name__ == '__main__':
    # 测试路径
    test_url = "https://m.weibo.cn/"
    # 最低分
    min_score = -5
    # 实例化
    scheduler = Scheduler(test_url, min_score)
    # 测试
    scheduler.run()

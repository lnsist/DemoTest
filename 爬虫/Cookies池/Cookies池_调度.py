"""
    Cookies调度整理所有功能
date: 18-10-21 上午11:30
"""
import multiprocessing

import 爬虫.Cookies池.Cookies池_生成模块 as Generator
import 爬虫.Cookies池.Cookies池_检测模块 as Tester
import 爬虫.Cookies池.Cookies池_接口模块 as Apier

# 周期
CYCLE = 20
# 检测模块开关
TESTER_ENABLED = True
# 获取模块开关 -- 一般第一次获取Cookies即可, 过时时间不会很短
GETTER_ENABLED = True
# 接口模块开关
API_ENABLED = True


class Scheduler(object):
    """
        调度整理Cookies池中基本模块的所有功能 -- 多进程
    因为Cookies的时效较长, 一般需要只需要循环数据库数据一次即可, 不用死循环数据库数据
    """

    @staticmethod
    def schedule_generator():
        """
            调度 Generator
        :return:
        """
        while True:
            Generator.main(CYCLE)

    @staticmethod
    def schedule_tester():
        """
            调度 Tester
        :return:
        """
        while True:
            Tester.main(CYCLE)

    @staticmethod
    def schedule_apier():
        """
            调度 Apier
        :return:
        """
        Apier.start_flask()

    def run(self):
        """
            运行调度
        :return:
        """
        # 进程池
        pool = multiprocessing.Pool()
        # 获取模块
        if GETTER_ENABLED:
            # 开启进程 指向 Generator
            # generator_process = Process(target=self.schedule_generator)
            # 开启进程
            # generator_process.start()

            # 添加进程
            pool.apply_async(self.schedule_generator)
        # 检测模块
        if TESTER_ENABLED:
            # 开启进程 指向 Tester
            # tester_process = Process(target=self.schedule_tester)
            # 开启进程
            # tester_process.start()

            # 添加进程
            pool.apply_async(self.schedule_tester)
        # 接口模块
        if API_ENABLED:
            # 开启进程 指向 Apier
            # api_process = Process(target=self.schedule_apier)
            # 开启进程
            # api_process.start()

            # 添加进程
            pool.apply_async(self.schedule_apier)
        # 关闭进程
        pool.close()
        # 阻塞进程 -- 等待所有进程关闭
        pool.join()


if __name__ == '__main__':
    # 开始调度
    Scheduler().run()

"""
    代理池4个模块: 存储模块, 获取模块, 检测模式, 接口模块
    存储模块: 使用Redis的有序集合, 用来做代理的去重和状态标识,
    获取模块: 定时从代理网站获取代理, 将获取的代理传递给存储模块进行存储
    检测模块: 定时通过存储模块获取所有代理, 并对代理进行检测, 根据不同的检测结果对代理设置不同的标识
    接口模块: 通过Web API提供服务接口, 接口通过连接数据库并通过Web形式返回可用的代理

    检测模块, 使用异步请求库aiohttp进行检测
date: 18-10-12 下午10:14
"""
import asyncio
import time

import aiohttp

from 爬虫.代理.代理池.代理池_存储模块 import RedisClient

# 状态码集合
VALID_STATUS_CODES = [200]
# 测试路径 -- 需要爬取的网络路径, 以防代理被此路径封IP
TEST_URL = "http://www.baidu.com"
# 步长
BATCH_TEST_SIZE = 100


class Tester(object):
    """
        测试模块, 使用异步请求库qiohttp进行网络访问检测代理是否可用
    """

    def __init__(self):
        # 获取Redis数据库
        self.redis = RedisClient()

    async def test_single_proxy(self, proxy, test_url=TEST_URL):
        """
            测试单个代理 -- 异步执行事件, 协程
        :param proxy: 代理
        :param test_url: 测试地址
        :return:
        """
        # 获取aiohttp的TCP连接 -- verify_ssl 是否检验
        conn = aiohttp.TCPConnector(verify_ssl=False)
        # 异步上下文管理打开会话, 获取会话
        async with aiohttp.ClientSession(connector=conn) as session:
            # 捕获异常
            try:
                # 如果代理是二进制
                if isinstance(proxy, bytes):
                    # 转码为字符串
                    proxy = proxy.decode("utf-8")
                # 拼接代理
                real_proxy = "http://" + proxy
                # 输出提示
                print("正在测试代理:", real_proxy)
                # 异步上下文管理请求访问, 获取响应报文 (测试路径, 设置代理, 超时时长)
                async with session.get(test_url, proxy=real_proxy, timeout=15) as response:
                    # 如果响应状态码在状态码集合中
                    if response.status in VALID_STATUS_CODES:
                        # 测试成功, 代理可用, 设置最高分
                        self.redis.max(proxy)
                        # 输出提示
                        print("代理可用:", proxy)
                    else:
                        # 测试失败, 代理不可用, 扣分
                        self.redis.decrease(proxy)
                        # 输出提示
                        print("响应状态码不合法, 代理不可用:", proxy)
            # except (ClientError, ClientConnectorError, TimeoutError, AttributeError):
            except Exception as e:
                # 输出异常提示
                print(e)
                # 测试失败, 请求出现异常, 代理不可用, 扣分
                self.redis.decrease(proxy)
                # 输出提示
                print("请求失败, 代理不可用:", proxy)

    def run(self, test_url, min_score=0):
        """
            测试函数
        :param min_score: 测试最小分数 -- 默认是0
        :param test_url: 测试地址
        :return:
        """
        # 输出提示
        print("检测器开始运行")
        # 捕获异常
        try:
            # 访问数据库获取所有数据
            proxies = self.redis.all(min_score=min_score)
            # 获取当前事件循环 -- 无限循环
            loop = asyncio.get_event_loop()
            # 批量测试, 从0开始, 到proxies的长度, 步长为100
            for i in range(0, len(proxies), BATCH_TEST_SIZE):
                # 切片[当前i到, i+步长100], 获取的代理列表
                test_proxies = proxies[i:i + BATCH_TEST_SIZE]
                # tasks是一个协程列表 -- 里面是异步执行的事件
                tasks = [self.test_single_proxy(proxy, test_url=test_url) for proxy in test_proxies]
                # 将协程注册到事件循环中,
                # run_until_complete 将协程对象注册到事件循环中, 由事件循环自动分配任务, 返回值是运行后的结果集
                # wait, gather 都是创建协程对象
                # wait 接收一个列表 gather接收一堆数据
                # wait 返回元组, 一个是成功集合, 另一个是未执行或者是失败的集合
                # gather 只返回成功集合
                loop.run_until_complete(asyncio.wait(tasks))
                # 休眠
                time.sleep(5)
        except Exception as e:
            # 输出异常提示
            print("测试器发生错误:", e)


if __name__ == '__main__':
    # 测试
    Tester().run(min_score=0)

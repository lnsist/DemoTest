"""
    代理池4个模块: 存储模块, 获取模块, 检测模式, 接口模块
    存储模块: 使用Redis的有序集合, 用来做代理的去重和状态标识,
    获取模块: 定时从代理网站获取代理, 将获取的代理传递给存储模块进行存储
    检测模块: 定时通过存储模块获取所有代理, 并对代理进行检测, 根据不同的检测结果对代理设置不同的标识
    接口模块: 通过Web API提供服务接口, 接口通过连接数据库并通过Web形式返回可用的代理

    存储模块, 使用非关系型数据库Redis, Redis是有序集合数据保存格式为 k=v,

date: 18-10-12 下午9:49
"""

import redis
from random import choice

# 最大分数
MAX_SCORE = 100
# 最小分数
MIN_SCORE = 0
# 初始分数
INITAL_SCORE = 10
# 主机
REDIS_HOST = "localhost"
# 端口
REDIS_PORT = 6379
# 密码
REDIS_PASSWORD = "123456"
# 数据库key
REDIS_KEY = "proxies"


class RedisClient(object):
    """
        存储模块 -- 数据库Redis客户端
    """

    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=15):
        """
            初始化
        :param host: 地址
        :param port: 端口
        :param password: 密码
        :param db: 数据库index, 15, 代理池数据库
        decode_responses 是否解码返回
        """
        # 连接数据库
        self.db = redis.StrictRedis(host=host, port=port, password=password, db=db, decode_responses=True)

    def add(self, proxy, score=INITAL_SCORE):
        """
            添加代理;, 设置初始分数
        :param proxy: 代理
        :param score: 分数
        :return: 添加结果
        """
        # 判断数据库中是否存在此代理
        if not self.db.zscore(REDIS_KEY, proxy):
            # 不存在, 则返回添加结果 -- 先分数(value), 后字段(key)   不然会报错...
            return self.db.zadd(REDIS_KEY, score, proxy)

    def random(self):
        """
            随机获取有效代理, 按分数高到低排序获取
        :return: 随机代理
        """
        # 查询数据库, 获取最高分
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        # 如果查询有结果
        if len(result):
            # 随机返回结果
            return choice(result)
        # 如果没有最高分
        else:
            # 查询数据库, 按照分数范围0-100获取有序集合的元素并排序, 默认排序是倒序
            result = self.db.zrevrange(REDIS_KEY, MIN_SCORE, MAX_SCORE)
            # 如果查询有结果
            if len(result):
                # 随机返回结果
                return choice(result)
            else:
                # 否则报错, 代理池为空
                raise Exception

    def decrease(self, proxy):
        """
            代理分数减1分,
        :param proxy: 代理
        :return: 修改后的代理分数
        """
        # 获取次代理数据
        score = self.db.zscore(REDIS_KEY, proxy)
        # 输出提示
        print("代理", proxy, " 当前分数", score, " 减1")
        # 当前分数减1
        return self.db.zincrby(REDIS_KEY, proxy, -1)

    def exists(self, proxy):
        """
            判断当前代理是否存在
        :param proxy: 代理
        :return: 是否存在
        """
        # 返回当前状态取反
        return not self.db.zscore(REDIS_KEY, proxy)

    def max(self, proxy):
        """
            设置当前代理分数为最大值
        :param proxy: 代理
        :return: 设置结果
        """
        # 输出提示
        print("代理", proxy, " 可用, 设置分数为 ", MAX_SCORE)
        # 这是当前代理分数为最大值, 并返回修改结果
        return self.db.zadd(REDIS_KEY, MAX_SCORE, proxy)

    def count(self):
        """
            获取总共代理数量
        :return: 总共代理数量
        """
        # 返回总共代理数量
        return self.db.zcard(REDIS_KEY)

    def all(self, min_score=MIN_SCORE):
        """
            获取全部代理 -- 指定分数到100
        :param min_score: 最小分数 -- 默认是0
        :return: 全部代理
        """
        # 返回全部代理
        return self.db.zrangebyscore(REDIS_KEY, min_score, MAX_SCORE)

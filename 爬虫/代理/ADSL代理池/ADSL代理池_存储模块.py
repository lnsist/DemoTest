"""
    ADSL存储模块 -- Redis数据库
date: 18-10-16 上午9:11
"""
import redis
import random

# 地址
REDIS_HOST = "localhost"
# 密码
REDIS_PASSWORD = "123456"
# 端口
REDIS_PORT = 6379
# 数据库key
PROXY_KEY = "adsl_proxies"


class RedisClient(object):
    """
        存储模块 -- Redis数据库操作
    """

    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, proxy=PROXY_KEY, db=15):
        """
            初始化数据库连接
        :param host: 地址
        :param port: 端口
        :param password: 密码
        :param proxy: 数据库key
        :param db: 数据库index -- 15, ADSL代理池数据库
        decode_responses 是否解码返回
        """
        # 获取数据库连接
        self.db = redis.StrictRedis(host=host, port=port, password=password, db=db, decode_responses=True)
        # 设置数据库key
        self.proxy_key = proxy

    def set_proxy(self, name, proxy):
        """
            设置代理
        :param name: 主机名称
        :param proxy: 代理
        :return: 设置结果
        """
        # 返回数据库操作结果, 保存主机名对应代理
        return self.db.hset(self.proxy_key, name, proxy)

    def get_proxy(self, name):
        """
            获取主机名称对应代理
        :param name: 主机名称
        :return: 代理
        """
        # 返回从数据库中获取到的代理, 对应主机名称
        return self.db.hget(self.proxy_key, name)

    def remove_proxy(self, name):
        """
            根据主机名称, 删除代理
        :param name: 主机名称
        :return: 删除结果
        """
        # 返回删除结果, 根据主机名删除对应代理
        return self.db.hdel(self.proxy_key, name)

    def proxy_count(self):
        """
            获取代理总数
        :return: 代理总数
        """
        # 返回从数据库中统计的代理总数
        return self.db.hlen(self.proxy_key)

    def get_name_list(self):
        """
            获取数据库中所有主机名称
        :return: 主机名称集合
        """
        # 返回数据库中的key集合, 主机名称集合
        return self.db.hkeys(self.proxy_key)

    def get_proxy_list(self):
        """
            获取所有代理
        :return: 代理集合
        """
        # 返回数据库中的value集合, 代理集合
        return self.db.hvals(self.proxy_key)

    def random_proxy(self):
        """
            获取随机代理
        :return: 随机代理
        """
        # 返回所有代理集合中, 随机一个代理
        return random.choice(self.get_proxy_list())

    def get_all(self):
        """
            获取所有数据
        :return: 字典型的所有数据
        """
        # 返回数据库中所有数据, 字典类型
        return self.db.hgetall(self.proxy_key)

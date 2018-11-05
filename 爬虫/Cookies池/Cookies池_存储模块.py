"""
    Cookies池基本模块: -------- 与代理池类似
1. 存储模块 -- 负责存储每个账号的用户名密码以及每个账号对应的Cookies信息
2. 生成模块 -- 负责生成新的Cookies, 从存储模块获取账号密码, 模拟登录目标页面, 登录成功, 将Cookies交给存储模块保存
3. 检测模块 -- 定时检测数据库中的Cookies是否有效, 针对不同的检测连接, 逐个拿取Cookies去访问页面,
                如果能成功访问则有效, 否则删除数据库中的Cookies, 等待生成模块重新生成
4. 接口模块 -- 提供对外服务的接口, 随机返回Cookies, 提供外部使用Cookies


存储模块 -- 存储的内容就是, 账号信息和Cookies信息
date: 18-10-20 下午8:31
"""

import random
import redis

# 主机
REDIS_HOST = "localhost"
# 端口
REDIS_PORT = 6379
# 密码
REDIS_PASSWORD = "123456"


class RedisClient(object):
    """
        存储模块
    """

    def __init__(self, table_type, website, host=REDIS_HOST, port=REDIS_PORT, db=15, password=REDIS_PASSWORD):
        """
            初始化, 获取数据库连接
        表名 -- table_type:website
                accounts:weibo(微博用户信息表), cookies:weibo(微博用户Cookies表)
                accounts:zhihu(知乎用户信息表), cookies:zhihu(知乎用户Cookies表)
        :param table_type: 表类型
        :param website: 信息类型 -- 站点
        :param host: 地址
        :param port: 端口
        :param password: 密码
        """
        # 数据库连接
        self.db = redis.StrictRedis(host=host, port=port, password=password, db=db, decode_responses=True)
        # 表类型
        # self.type = type
        # 信息类型
        # self.website = website
        # 表名 -- 表类型:信息类型
        self.table_name = "{table_type}:{website}".format(table_type=table_type, website=website)

    def set_data(self, key, value):
        """
            保存数据
        :param key: 键名
        :param value: 值
        :return: 保存结果
        """
        # 保存hash数据
        return self.db.hset(self.table_name, key, value)

    def get_data(self, key):
        """
            根据键名, 获取数据
        :param key: 键名
        :return: 数据
        """
        # 获取hash数据
        return self.db.hget(self.table_name, key)

    def delete_data(self, key):
        """
            根据键名删除数据
        :param key: 键名
        :return: 删除结果
        """
        # 删除hash数据
        return self.db.hdel(self.table_name, key)

    def get_all_key(self):
        """
            获取所有键名
        :return: 所有键名
        """
        # 所有键名
        return self.db.hkeys(self.table_name)

    def random_data(self):
        """
            随机返回一个数据
        :return: 随机一个数据
        """
        # 随机一个数据
        return random.choice(self.db.hvals(self.table_name))

    def all_data(self):
        """
            返回所有数据
        :return: 所有数据
        """
        # 所有数据
        return self.db.hgetall(self.table_name)


if __name__ == '__main__':
    # 数据库连接 -- 用户信息表
    accounts_db = RedisClient(table_type="accounts", website="weibo")

    weibo_ = {
        "15285326066": "iqr70760",
        "18212510571": "ubu42110",
        "13639258404": "zbm13604"
    }

    for username, password in weibo_.items():
        accounts_db.set_data(username, password)

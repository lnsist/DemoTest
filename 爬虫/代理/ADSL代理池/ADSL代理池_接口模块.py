"""
    接口模块 -- 整理调度其他模块, 返回至Tornado的Server模块搭建的Web
date: 18-10-16 下午7:51
"""
import json
import tornado.ioloop
import tornado.web
from tornado.web import RequestHandler, Application
from 爬虫.代理.ADSL代理池.ADSL代理池_存储模块 import RedisClient
from 爬虫.代理.ADSL代理池.ADSL代理池_拨号模块 import Sender

# API端口
API_PORT = 8000


class MainHandler(RequestHandler):
    """
        接口模块 -- 提供web服务以供调用
    """

    def initialize(self, redis):
        """
            初始化数据
        :param redis: 数据库
        :return:
        """
        # 初始化数据库
        self.redis = redis

    def get(self, api=""):
        """
            设置get访问路由, 路径对应方法
        :param api: 请求路径
        :return: 路径对应页面
        """
        # 路径为空
        if not api:
            # 路径列表
            links = {"random": "随机获取代理", "proxies": "获取所有代理", "names": "获取所有主机名称", "all": "获取所有数据", "count": "获取代理总数"}
            # 返回源码
            self.write("<h2>欢迎来到谢振恒的ADSL代理池</h2>")
            # 循环返回 a标签, 方便调用接口
            for k, v in links.items():
                # 循环写入a标签
                self.write("<a href=" + k + ">" + v + "</a><br>")

        # 随机返回代理 -- 路径
        if api == "random":
            # 访问数据库, 获取数据
            result = self.redis.random()
            # 数据不为空
            if result:
                # 写入数据
                self.write(result)

        # 返回所有主机名称 -- 路径
        if api == "names":
            # 访问数据库, 获取数据
            result = self.redis.names()
            # 数据不为空
            if result:
                # 写入数据
                self.write(json.dumps(result))

        # 返回所有代理 -- 路径
        if api == "proxies":
            # 访问数据库, 获取数据
            result = self.redis.proxies()
            # 数据不为空
            if result:
                # 写入数据
                self.write(json.dumps(result))

        # 返回所有数据, 字典类型 -- 路径
        if api == "all":
            # 访问数据库, 获取数据
            result = self.redis.all()
            # 数据不为空
            if result:
                # 写入数据
                self.write(json.dumps(result))

        # 返回代理总数 -- 路径
        if api == "count":
            # 写入数据
            self.write(str(self.redis.count()))


def main(redis, port=API_PORT, address=""):
    """
        主入口
    :param redis: 数据库
    :param port: api端口
    :param address: 主机
    :return:
    """
    # 设置监听路径
    application = Application([
        (r"/", MainHandler, dict(redis=redis)),
        (r"/(.*)", MainHandler, dict(redis=redis))
    ])
    # 开始监听
    application.listen(port, address=address)
    # 输出提示
    print("接口模块监听中...")
    # tornado web服务器开启
    tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
    # 开始拨号
    Sender().adsl()
    # 开启接口
    main(RedisClient())

"""
    Cookies池基本模块: -------- 与代理池类似
1. 存储模块 -- 负责存储每个账号的用户名密码以及每个账号对应的Cookies信息
2. 生成模块 -- 负责生成新的Cookies, 从存储模块获取账号密码, 模拟登录目标页面, 登录成功, 将Cookies交给存储模块保存
3. 检测模块 -- 定时检测数据库中的Cookies是否有效, 针对不同的检测连接, 逐个拿取Cookies去访问页面,
                如果能成功访问则有效, 否则删除数据库中的Cookies, 等待生成模块重新生成
4. 接口模块 -- 提供对外服务的接口, 随机返回Cookies, 提供外部使用Cookies


接口模块 --  定义一个web接口, 方便爬虫获取使用Cookies
date: 18-10-21 上午11:19
"""
from flask import Flask
from flask import g
# get_conn 中要用到RedisClient, 所以必须导入
from 爬虫.Cookies池.Cookies池_存储模块 import RedisClient

# 生成模块的匹配字典
GENERATOR_MAP = {
    # 站点: 生成模块 具体模拟登陆
    "weibo": "WeiboCookiesGenerator"
}
# 设置自定义名称
app = Flask(__name__)


def get_conn():
    """
        获取全局变量 g 对象
    :return: g 对象
    """
    # 循环模块匹配自定啊
    for website in GENERATOR_MAP:
        # 如果全局变量中没有此属性
        if not hasattr(g, website + "_cookies"):
            # 设置属性 -- 'website'_cookies = RedisClient(cookies, 'website')
            setattr(g, website + "_cookies", eval("RedisClient('cookies', '" + website + "')"))
    # 返回全局变量
    return g


@app.route("/")
def index():
    """
        首页
    :return:
    """
    result = "<h2>欢迎来到谢振恒的Cookies池</h2>"
    result += "<h3><p>随机获取website(站点)可用的Cookies</p></h3><ul>"
    for website in GENERATOR_MAP:
        result += "<li><a href='/" + website + "/random'>" + website + "可用的Cookies</a></li>"
    result += "</ul>"
    return result


@app.route("/<website>/random")
def random(website):
    """
        获取随机Cookies, 访问路径为 /weibo/random
    :param website: 站点
    :return: 随机Cookies
    """
    # 获取全局变量
    g_ = get_conn()
    # 获取随机Cookies并返回
    cookies = getattr(g_, website + "_cookies").random_data()
    # 返回Cookies
    return cookies


def start_flask():
    """
        启动Flask
    :return:
    """
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    start_flask()

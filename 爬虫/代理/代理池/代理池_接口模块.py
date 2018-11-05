"""
    代理池4个模块: 存储模块, 获取模块, 检测模式, 接口模块
    存储模块: 使用Redis的有序集合, 用来做代理的去重和状态标识,
    获取模块: 定时从代理网站获取代理, 将获取的代理传递给存储模块进行存储
    检测模块: 定时通过存储模块获取所有代理, 并对代理进行检测, 根据不同的检测结果对代理设置不同的标识
    接口模块: 通过Web API提供服务接口, 接口通过连接数据库并通过Web形式返回可用的代理

    接口模块, 为了方便获取所有代理列表, 以Web API暴露可用代理, 若直接暴露存储模块, 耦合严重且不安全
    1. 使用者需要知道你的存储模块账号密码  --不安全
    2. 如果代理池是部署在远程服务器, 数据库只允许本地连接, 远程就无法直接访问存储模块  --无法远程操作
    3. 如果爬虫所在主机没有连接Redis模块, 或者编程语音部署Python, 也无法使用存储模块  --接口不对接
    4. 如果存储模块更新, 爬虫端程序也需要同样做修改  --耦合严重
date: 18-10-14 上午9:07
"""
from flask import Flask, g
from 爬虫.代理.代理池.代理池_存储模块 import RedisClient

# Flask对象名
__all__ = ["app"]
# 加载当前文件 -- 实例化, 参数当前文件名
app = Flask(__name__)


def start_flask():
    """
        启动Flask
    :return:
    """
    app.run(host='0.0.0.0', port=5555)


def get_conn():
    """
        获取连接
    :return: 数据库连接
    """
    # 如果 g 没有此属性 redis
    if not hasattr(g, "redis"):
        # 获取数据库 Redis
        g.redis = RedisClient()
    # 返回数据库
    return g.redis


# 装饰器, 装饰请求路径, 增加路由 -- 首页
@app.route("/")
def index():
    """
        首页
    :return: 欢迎页面
    """
    result = "<h2>欢迎来到谢振恒的代理池</h2>"
    result += "<a href='/random'>随机获取可用的代理</a><br><br>"
    result += "<a href='/count'>获取代理池总数</a><br><br>"
    return result


# 装饰器, 装饰请求路径, 增加路由 -- /random
@app.route("/random")
def get_proxy():
    """
        随机获取可用的代理
    :return: 可用代理
    """
    # 获取数据库连接
    conn = get_conn()
    # 返回可用代理
    return conn.random()


# 装饰器, 装饰请求路径, 增加路由 -- /count
@app.route("/count")
def get_counts():
    """
        获取代理池总数
    :return: 代理池总数
    """
    # 获取数据库连接
    conn = get_conn()
    # 返回当前代理池的总数
    return "当前代理池的总数 " + str(conn.count())


if __name__ == '__main__':
    start_flask()
    # app.run(host='0.0.0.0', port=5000)

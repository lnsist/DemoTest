"""
    mini_web动态数据框架
date: 18-10-9 下午6:39
"""
import datetime
import time
import re

import pymysql

# 文件目录
http_path = "./static"

# 准备一个全局的空路由列表
g_route_list = []


def main(env):
    """
        程序入口, 与web服务器对接接口函数
    :param env:
    :return:
    """
    # 获取访问路径
    request_path = env["PATH_INFO"]
    # 输出提示
    print("web请求路径:", request_path)
    # 遍历路由, 判断调用对应函数
    for url, func in g_route_list:
        # 判断访问路径是否存在
        if request_path in url:
            # 返回对应函数获取的源码
            return "200 OK", func(request_path)
    else:
        # 不存在, 返回404
        return "404 Not Found", error_page()


# 装饰器工厂, 动态增加路由列表
def route(url):
    """
        自定义参数装饰器工厂
    :param url: 路径
    :return: 装饰器
    """

    def wrapper(func):
        """
            返回内部函数
        :param func: 被装饰函数
        :return: 内部函数
        """
        # 增加路由 (路径, 函数)
        g_route_list.append((url, func))

        def inner(request_path):
            """
                具体的装饰步骤
            :return:
            """
            # 装饰步骤
            print("进行扩展功能")
            # 被装饰函数
            func(request_path)

        return inner

    return wrapper


@route("/templates_index.html")
def templates_index(request_path):
    """
        返回股票首页 -- 访问数据库获取数据
    :return:
    """
    # 数据库数据
    data_from_mysql = ""
    # 数据库访问
    conn = pymysql.connect(host="localhost", user="root", password="123456", database="stock_db", port=3306, charset="utf8")
    # 获取游标
    cur = conn.cursor()
    # 执行sql语句 -- 查询所有数据, 返回影响行数
    affect_rows = cur.execute("select * from info")
    # 输出提示
    print("templates_index影响行数:", affect_rows)
    # 循环数据, 拼接源码
    for item in cur.fetchall():
        # 获取数据
        line = """<tr>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>>
        <td><input type='button' value='添加' id='toAdd' name='toAdd' systemidvaule='000036'/></td
        </tr>
        """ % item
        # 拼接源码
        data_from_mysql += line
    # 获取模板页面, 拼接源码
    with open(http_path + request_path, "r") as f:
        # 获取页面源码
        response_body = f.read()
    # 通过正则表达式, 拼接源码并返回
    response_body = re.sub("{%content%}", data_from_mysql, response_body)
    # 关闭游标
    cur.close()
    # 返回源码
    return response_body.encode("utf-8")


@route("/center.html")
def center(request_path):
    """
        返回股票个人中心 -- 访问数据库获取数据
    :return:
    """
    # 数据库数据
    data_from_mysql = ""
    # 数据库访问
    conn = pymysql.connect(host="localhost", user="root", password="123456", database="stock_db", port=3306, charset="utf8")
    # 获取游标
    cur = conn.cursor()
    # 执行sql语句 -- 查询所有数据, 返回影响行数
    sql = "select i.code,i.short,i.chg,i.turnover ,i.price,i.highs,f.note_info from info as i inner join focus as f  on i.id=f.info_id"
    affect_rows = cur.execute(sql)
    # 输出提示
    print("center影响行数:", affect_rows)
    # 循环数据, 拼接源码
    for item in cur.fetchall():
        # 获取数据
        line = """<tr>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>
            <a type="button" class="btn btn-default btn-xs" href="/update/300268.html"> <span class="glyphicon glyphicon-star" aria-hidden="true"></span> 修改 </a>
        </td>
        <td>
            <input type="button" value="删除" id="toDel" name="toDel" systemidvaule="300268">
        </td>
        </tr>
        """ % item
        # 拼接源码
        data_from_mysql += line
    # 获取模板页面, 拼接源码
    with open(http_path + request_path, "r") as f:
        # 获取页面源码
        response_body = f.read()
    # 通过正则表达式, 拼接源码并返回
    response_body = re.sub("{%content%}", data_from_mysql, response_body)
    # 关闭游标
    cur.close()
    # 返回源码
    return response_body.encode("utf-8")


@route("/gettime.html")
def get_time(request_path):
    """
        获取当前时间
    :return: 返回当前时间源码
    """
    return ("当前时间: %s" % datetime.datetime.now()).encode("utf-8")


@route("/index.html, /index2.html, /grand.html")
def get_start_html(request_path):
    # 获取模板页面, 拼接源码
    with open(http_path + request_path, "rb") as f:
        # 获取页面源码
        response_body = f.read()
    # 返回源码
    return response_body


def error_page():
    """
        404 错误页面
    :return:　错误页面
    """
    # 返回错误页面
    return '<a href="http://www.douyu.com/directory/game/yz"><img src="/images/404.jpg"></a>'.encode("utf-8")

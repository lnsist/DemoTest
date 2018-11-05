"""
    最基础的urllib设置代理
date: 18-10-11 下午7:24
"""

from urllib.error import URLError
from urllib.request import ProxyHandler, build_opener
import socks
import socket
from urllib import request


def proxy_HTTP():
    """
        HTTP代理
    :return:
    """
    # 代理 -- 用户名:密码
    # proxy = "username:password@127.0.0.1:9743"
    proxy = "127.0.0.1:9743"
    # 代理头
    proxy_handler = ProxyHandler({
        "http": "http://" + proxy,
        "https": "https://" + proxy
    })
    # 创建连接, 设置代理头
    opener = build_opener(proxy_handler)
    # 捕获url异常
    try:
        # 请求访问
        response = opener.open("http://httpbin.org/get")
        # 输出响应报文
        print(response.read().decode("utf-8"))
    except URLError as e:
        # 异常提示
        print(e.reason)


def proxy_SOCKS5():
    """
        SOCKS代理
    :return:
    """
    # 设置 socks5 代理
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9742)
    # 使用代理
    socket.socket = socks.socksocket
    # 捕获URL异常
    try:
        # 请求访问
        response = request.urlopen("http://httpbin.org/get")
        # 输出响应报文
        print(response.read().decode("utf-8"))
    except URLError as e:
        # 输出异常提示
        print(e.reason)


if __name__ == '__main__':
    # HTTP 代理
    proxy_HTTP()
    # SOCKS5 代理
    # proxy_SOCKS5()

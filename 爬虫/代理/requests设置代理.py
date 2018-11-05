"""
    requests设置代理
date: 18-10-11 下午7:54
"""
import socket

import requests
import socks


def proxy_HTTP():
    """
        http代理
    :return:
    """
    # 代理 -- username 用户名 password 密码
    proxy = "username:password@127.0.0.1:9743"
    # 设置对应http代理
    proxies = {
        "http": "http://" + proxy,
        "https": "https://" + proxy
    }
    # 捕获访问异常
    try:
        # 使用代理, 请求访问
        respones = requests.get("http://httpbin.org/get", proxies=proxies)
        # 输出响应报文
        print(respones.text)
    except requests.exceptions.ConnectionError as e:
        # 输出错误提示
        print(e.args)


def proxy_SOCKS5_1():
    """
        socks5代理1
    :return:
    """
    # 代理
    proxy = "127.0.0.1:9742"
    # 设置socks5代理
    proxies = {
        "http": "socks5://" + proxy,
        "https": "socks5://" + proxy
    }
    # 捕获访问异常
    try:
        # 使用代理, 请求访问
        respones = requests.get("http://httpbin.org/get", proxies=proxies)
        # 输出响应报文
        print(respones.text)
    except requests.exceptions.ConnectionError as e:
        # 输出错误提示
        print(e.args)


def proxy_SOCKS5_2():
    """
        socks5代理2
    :return:
    """
    # 这是socks5代理
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9742)
    # 使用代理
    socket.socket = socks.socksocket
    # 捕获请求访问异常
    try:
        # 请求访问
        response = requests.get("http://httpbin.org/get")
        # 输出相应报文
        print(response.text)
    except requests.exceptions.ConnectionError as e:
        print(e.args)


if __name__ == '__main__':
    # http代理
    proxy_HTTP()
    # socks5代理_1
    proxy_SOCKS5_1()
    # socks5代理_2
    proxy_SOCKS5_2()

"""
    工具类
date: 18-10-12 下午9:36
"""
import time

import requests
from requests.exceptions import ConnectionError

# 请求头
base_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7"
}


def get_page(url, options={}):
    """
        请求访问
    :param url: 请求路径
    :param options: 请求头选项
    :return: 源码
    """
    # 拼接传入的请求头信息 **options 拆包
    headers = dict(base_headers, **options)
    # 输出提示
    print("正在抓取 " + url)
    # 捕获异常
    try:
        # 请求访问, 请求路径, 请求头
        response = requests.get(url, headers=headers)
        # 休眠
        time.sleep(1)
        # 如果状态码为200
        if response.status_code == 200:
            # 输出提示
            print("抓取成功 ", url, " ", response.status_code)
            # 返回源码
            return response.text
    except ConnectionError:
        # 输出提示
        print("抓取失败 " + url)
        return None

    # 返回源码
    return response.text

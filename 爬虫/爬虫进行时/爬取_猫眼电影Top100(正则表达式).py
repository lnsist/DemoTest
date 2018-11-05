"""猫眼电影Top100 -- 初次爬虫 ( 正则表达式提取信息 )
date: 18-9-26 下午8:37

爬虫步骤--大概分为四步:
    一、请求访问
    二、获取数据
    三、解析数据
    四、存储数据
"""
import json
import time

import requests
import re


def get_one_page(url):
    """
        网络访问
    :param url: 网址
    :return: 网页源码
    """
    # 请求头
    headers = {"user-Agent": "Mozilla/5.o(Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko)"
                             "Chrome/69.0.3497.100 Safari/537.36"}
    # 网络访问
    response = requests.get(url, headers=headers)
    # 访问成功
    if response.status_code == 200:
        # 返回网页源码
        return response.text


def pares_one_page_by_reex(html):
    """
        解析html源码 -- 生成器 ( 正则表达式抓取数据 )
    :param html: 源码
    :return:
    """
    # 表达式
    pattern = re.compile(
        '<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?'
        'star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>', re.S)
    # 匹配
    items = re.findall(pattern, html)
    # 封装成字典
    for item in items:
        # 输出提示
        print(item)
        yield {
            # 排名
            "index": item[0],
            # 图片
            "image": item[1],
            # 电影名称
            "title": item[2].strip(),
            # 主演：张国荣,张丰毅,巩俐    --   从 主演: 后开始截取字段
            "actor": item[3].strip()[3:] if len(item[3].strip()) > 3 else "",
            # 上映时间：1993-01-01    --    从 上映时间: 后开始截取字段
            "time": item[4].strip()[5:] if len(item[4].strip()) > 5 else "",
            # 拼接评分
            "score": item[5].strip() + item[6].strip()
        }


def write_to_file(file_name, content):
    """
        写入文件
    :param file_name: 文件名
    :param content: html源码
    :return:
    """
    # 上下文管理器, a方式追加打开文件, 编码格式 utf-8
    with open(file_name, "a", encoding="utf-8") as f:
        # 写入文件, 内容是 content 的json.dumps格式化后的数据, ensure_ascii中文不转义
        f.write(json.dumps(content, ensure_ascii=False) + "\n")


def main(offset):
    """
        程序主入口 -- 分页查询
    :param offset: 分页查询
    :return:
    """
    # 猫眼电影Top100
    url = "http://maoyan.com/board/4?offset=" + str(offset)
    # 调用网络访问, 获取网页源码
    html = get_one_page(url)
    # 保存源代码
    # write_to_file("source_code.txt", html)
    # 解析html源代码 -- 生成器
    for item in pares_one_page_by_reex(html):
        # 写入文件
        write_to_file("result.txt", item)


if __name__ == '__main__':
    # 分页查询
    for i in range(10):
        #
        main(i * 10)
        # 休眠 1 秒 -- 避免访问过快, 被反爬虫
        time.sleep(1)

"""
爬取今日头条的街拍图片 -- Ajax爬取数据 ( 多线程 )
date: 18-9-27 下午7:37
"""
import os
from _md5 import md5
import requests
from urllib.parse import urlencode

from multiprocessing.pool import Pool


def get_page(offset):
    """
        网络访问 -- 模拟Ajax请求 获取响应源码
    :param offset: 分页 -- 偏移量
    :return: 页面源码
    """
    # 请求体
    params = {
        "offset": offset,
        "format": "json",
        "keyword": "街拍",
        "autoload": "true",
        "count": "20",
        "cur_tab": "1",
        "from": "search_tab"
    }
    # 网址拼接请求体 -- urlencode 将字符串转成请求体 k=v&k=v
    url = "https://www.toutiao.com/search_content/?" + urlencode(params)
    # 异常捕抓
    try:
        # 网络访问
        response = requests.get(url)
        # 判断状态码是否 200 成功访问
        if response.status_code == 200:
            # 以json格式返回响应体 -- 网页源代码
            return response.json()
    except requests.ConnectionError:
        return


def get_images(json):
    """
        在页面源码中获取图片
    :param json: json格式的页面源码
    :return: 生成器返回, 标题 和 图片地址
    """
    # 判断是否有data
    if json.get("data"):
        for item in json.get("data"):
            title = item.get("title")
            images = item.get("image_list")
            if images:
                for image in images:
                    if isinstance(image, dict):
                        yield {
                            "title": title,
                            "image": image.get("url")
                        }


def save_image(item):
    """
        下载并保存图片
    :param item: 是一个字典, 其中title是文件夹名称, image是图片
    :return:
    """
    # 根目录
    path = "今日头条街拍/"
    # 判断是否存在此文件夹
    if not os.path.exists(path + item.get("title")):
        # 如果不存在新建文件夹
        os.makedirs(path + item.get("title"))
    # 捕抓网络访问异常
    try:
        # 下载图片
        response = requests.get("http:" + item.get("image"))
        # 响应码
        if response.status_code == 200:
            # 拼接文件路径
            file_path = "{0}/{1}.{2}".format(path + item.get("title"), md5(response.content).hexdigest(), ".jpg")
            # 判断图片是否存在
            if not os.path.exists(file_path):
                # 创建图片
                with open(file_path, "wb") as f:
                    # 将下载的图片写入文件中
                    f.write(response.content)
            else:
                # 如果图片已存在
                print("此图片已经下载", file_path)
    except requests.ConnectionError:
        print("图片下载错误")


def main(offset):
    # 获取网页源码
    json = get_page(offset)
    # 循环下载图片 -- 生成器
    for item in get_images(json):
        # 输出字典 -- 标题 图片地址
        print(item)
        # 下载并保存图片
        save_image(item)


# 开始页数
GROUP_START = 0
# 结束页数
GROUP_END = 1

if __name__ == '__main__':
    # 线程池
    pool = Pool()
    # 列表生成式, 从 1 到 20, 最终乘以 20
    groups = ([x * 20 for x in range(GROUP_START, GROUP_END + 1)])
    # 创建线程到线程池
    pool.map(main, groups)
    # 关闭线程池
    pool.close()
    # 阻塞线程池
    pool.join()

"""贴吧爬虫
用XPath来做一个简单的爬虫，爬取某个贴吧里的所有帖子，获取每个帖子的标题，连接和帖子中图片

@Date    : 2019-01-27 20:27
@Author  : lnsist
"""
import requests
from lxml import etree
import json


class TieBaSpider(object):
    """贴吧爬虫"""

    def __init__(self, name):
        # 贴吧名字
        self.name = name
        # 贴吧url
        self.list_url_pattern = "   http://tieba.baidu.com/mo/q----,sz@320_240-1-3---/m?kw=" + name + "&pn={}"
        # host
        self.host = "http://tieba.baidu.com"
        # 贴吧极速版
        self.pre_url = "http://tieba.baidu.com/mo/q---8DC83EB65C86E38C9EC4A227050C8970%3AFG%3D1-sz%40320_240%2C-1-3-0--2--wapp_1523749569931_549/"
        # 请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Mobile Safari/537.36"
        }

    def get_page_html(self, url):
        """根据url发送请求

        :param url: url
        :return: 返回请求响应
        """
        # 发起请求
        response = requests.get(url, headers=self.headers)
        # return response.content.decode() # ValueError: Unicode strings with encoding declaration are not supported. Please use bytes input or XML fragments without declaration.
        # <?xml version="1.0" encoding="UTF-8"?>
        # 返回请求响应
        return response.content

    def get_content_list(self, page_html):
        """获取标题,URL,详情页的图片"""

        # 加载HTML
        page_element = etree.HTML(page_html)
        # 获取divs
        divs = page_element.xpath("//div[contains(@class, 'i')]")
        # 初始化内容list
        content_list = []
        # 循环divs
        for div in divs:
            # 初始化字典
            dic = {}
            # 获取标题
            dic['title'] = div.xpath("./a/text()")[0] if len(div.xpath("./a/text()")) != 0 else None
            # 获取url
            dic['url'] = self.host + div.xpath("./a/@href")[0] if len(div.xpath("./a/@href")) else None
            # 获取详情页中所有图片
            images = self.get_images(dic['url'])
            # 获取图片
            dic["images"] = [requests.utils.unquote(image).split("&src=")[-1] for image in images]
            # print(dic["images"])
            # 添加列表
            content_list.append(dic)
        # 返回列表 [标题, url, 图片]
        return content_list

    def get_images(self, detail_url):
        """根据详情页url获取所有图片

        :param detail_url: 详情页url
        :return: 当前详情页中所有图片
        """

        # 发送请求,获取内容
        detail_html = self.get_page_html(detail_url)
        # 加载HTML
        detail_element = etree.HTML(detail_html)
        # 获取图片
        images = detail_element.xpath("//img[@class='BDE_Image']/@src")
        # 获取下一页url
        next_detail_urls = detail_element.xpath("//a[text()='下一页']/@href")
        # print(next_detail_urls)
        # 如果有下一页
        if len(next_detail_urls) != 0:
            # 获取第一个下一页url
            next_detail_url = self.pre_url + next_detail_urls[0]
            # 递归获取详情页中所有图片
            images += self.get_images(next_detail_url)  # 每调用一次就会返回下一页所有图片的URL的地址列表
        # 返回当前详情页中所有图片
        return images

    def save_conent_list(self, content_list):
        """保存内容列表

        :param content_list: 内容列表
        :return:
        """

        # 打开文件
        with open(self.name + ".txt", 'a', encoding="utf8") as f:
            # 循环内容列表
            for content in content_list:
                # 写入文件 -- json转换
                json.dump(content, f, ensure_ascii=False)
                # 换行
                f.write("\n")

    def run(self):
        # 0. 定义变量 pn=0
        pn = 0
        while True:
            # 1. 准备URL
            list_url = self.list_url_pattern.format(pn)
            # 2. 发送请求获取内容
            page_html = self.get_page_html(list_url)
            # 3. 根据内容提取数据
            content_list = self.get_content_list(page_html)
            # 4. 保存内容
            self.save_conent_list(content_list)
            # 5. pn序号递增20, 循环1-4
            pn += 20
            if len(content_list) < 20:
                break


if __name__ == '__main__':
    tbs = TieBaSpider("做头发")
    tbs.run()

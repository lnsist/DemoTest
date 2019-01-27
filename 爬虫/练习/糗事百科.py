"""
提取糗百中热门主题中所有段子信息,每个段子包含发送人头像URL,昵称,性别,段子内容, 好笑数,评论数
@Date    : 2019-01-27 20:41
@Author  : lnsist
"""

import requests
from lxml import etree
import json
import re


class QiuBaiSpider(object):
    """糗事百科爬虫"""

    def __init__(self):
        """初始化"""

        # 初始化url
        self.url_pattern = "https://www.qiushibaike.com/hot/page/{}/"
        # 请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
        }

    def get_url_list(self):
        """根据格式返回url列表"""

        # url_list = []
        # for i in range(1, 14):
        #     url = self.url_pattern.format(i)
        #     url_list.append(url)
        # return url_list
        # 返回url列表
        return [self.url_pattern.format(i) for i in range(1, 14)]

    def get_html(self, url):
        """发送请求获取响应

        :param url: url
        :return: 请求响应
        """

        # 发送请求
        response = requests.get(url, headers=self.headers)
        # 返回响应
        return response.content

    def get_content_list(self, html):
        """根据HTML返回内容列表

        :param html: 响应
        :return: 内容列表
        """

        # 加载HTML
        page_elment = etree.HTML(html)
        # 获取divs
        divs = page_elment.xpath("//div[@id='content-left']/div")
        # 初始化内容列表
        content_list = []
        # 循环divs
        for div in divs:
            # print(etree.tostring(div).decode())
            # 获取用户头像
            user_head = div.xpath(".//div[@class = 'author clearfix']//img/@src")
            # 判断是否有用户头像
            user_head = user_head[0] if len(user_head) != 0 else None
            # 获取昵称
            user_name = div.xpath(".//div[@class = 'author clearfix']//h2/text()")
            # 判断是否有昵称
            user_name = user_name[0] if len(user_name) != 0 else None
            # 获取性别
            user_gender = div.xpath(".//div[starts-with(@class, 'articleGender')]/@class")
            # 性别切割字符串
            user_gender = re.findall("articleGender\s*(\\w+)Icon", user_gender[0])[0] if len(user_gender) != 0 else None
            # print(user_gender)
            # 获取内容
            content = div.xpath(".//div[@class='content']/span//text()")
            # 判断是否有内容
            content = content[0] if len(content) != 0 else None
            # print(content)
            # 获取好笑数
            vote = div.xpath(".//span[@class='stats-vote']/i/text()")
            # 判断是否有好笑数
            vote = vote[0] if len(vote) != 0 else None
            # 获取评论数
            comments = div.xpath(".//span[@class='stats-comments']//i/text()")
            # 判断是否有评论数
            comments = comments[0] if len(comments) != 0 else None
            # 拼接字典
            dic = {"user_head": user_head, "user_name": user_name, "user_gender": user_gender,
                   "content": content, "vote": vote, "comments": comments}
            # 添加内容列表
            content_list.append(dic)
        # 返回内容列表
        return content_list

    def sav_conent_list(self, content_list):
        """持久化内容列表

        :param content_list: 内容列表
        :return:
        """

        # 打开文件
        with open("qiubai.txt", 'a', encoding='utf-8') as f:
            # 循环内容列表
            for conent in content_list:
                # 写入文件 -- json转换
                json.dump(conent, f, ensure_ascii=False)
                # 换行
                f.write("\n")

    def run(self):
        # - 准备URL列表
        url_list = self.get_url_list()
        # - 遍历列表, 获取每一个URL对应的内容
        for url in url_list:
            html = self.get_html(url)
            # - 提取数据
            content_list = self.get_content_list(html)
            # - 保存数据
            self.sav_conent_list(content_list)


if __name__ == '__main__':
    qs = QiuBaiSpider()
    qs.run()

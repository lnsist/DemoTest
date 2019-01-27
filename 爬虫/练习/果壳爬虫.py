"""果壳爬虫
需求 写一个爬虫通过正则匹配果壳问答上面的所有精彩回答的URL地址和标题: https://www.guokr.com/ask/highlight/?page=1

@Date    : 2019-01-27 20:19
@Author  : lnsist
"""

import requests
import re
import json


class GuokeSpider(object):
    """果壳爬虫"""

    def __init__(self):
        """初始化"""

        # 设置请求头
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36"
        }
        # 基准URL
        self.basic_url = 'https://www.guokr.com/'

    def get_page_from_url(self, url):
        '''根据URL返回页面内容'''

        # 发起请求
        response = requests.get(url, headers=self.headers)
        # 返回请求响应
        return response.content.decode()

    def get_ask_list_from_page(self, page):
        '''根据页面内容,返回标题和对应URL的列表'''

        # 获取到包含标题和URL
        url_title_list = re.findall('<h2><a target="_blank" href="(.+?)">(.+?)</a></h2>', page)
        # print(url_title_list)
        # 获取下一页
        next_url = re.findall('<a href="(.+?)">下一页</a>', page)
        # 判断是否有下一页
        next_url = self.basic_url + next_url[0] if len(next_url) != 0 else None
        # 返回标题和url, 下一页
        return url_title_list, next_url

    def save_ask_list(self, ask_list):
        '''把标题和URL保存到文件,每条信息保存一行'''

        # 打开文件
        with open("gouke.json", 'a', encoding='utf8') as f:
            # 循环响应
            for ask in ask_list:
                # 写入文件
                json.dump(ask, f, ensure_ascii=False)
                # 换行
                f.write('\n')

    def run(self):
        # - 1.准备URL
        url = 'https://www.guokr.com/ask/highlight/'
        while url:
            # - 2.发送请求获取响应数据
            print(url)
            page = self.get_page_from_url(url)
            # - 3. 解析响应数据, 获取标题和对应URL列表
            ask_list, url = self.get_ask_list_from_page(page)
            # - 4.保存标题和URL以json格式保存到文件中, 每条信息转一行
            self.save_ask_list(ask_list)


if __name__ == '__main__':
    gks = GuokeSpider()
    gks.run()

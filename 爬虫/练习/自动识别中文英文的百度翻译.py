"""自动识别中文英文的百度翻译
百度翻译自动检测语音需要发送一次请求后台确认需要翻译的语言
所以, 需要先发送一次请求确认需要翻译的语言后再进行翻译

@Date    : 2019-01-25 19:14
@Author  : lnsist
"""
import sys

import requests


class FanYiSpider(object):

    def __init__(self, word):
        """初始化百度翻译爬虫
        :param word: 需要翻译的词语
        """
        # 检测语言URL
        self.detect_url = 'https://fanyi.baidu.com/langdetect'
        # 准备翻译的URL
        self.trans_url = 'https://fanyi.baidu.com/basetrans'
        # 请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900P Build/LRX21T) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Mobile Safari/537.36'
        }
        # 要翻译的内容
        self.word = word

    def get_page_from_url(self, url, data):
        """根据URl, 获取请求响应

        :param url: URL
        :param data: 请求体
        :return: 请求响应
        """
        # 接受发送请求后返回的响应( url, 请求体, 请求头)
        response = requests.post(url=url, data=data, headers=self.headers)
        # 返回响应
        return response

    def run(self):
        """程序入口"""
        # 调用百度翻译测试语言接口, 获取当前词语语言
        # 设置请求体
        data = {"query": self.word}
        # 发起请求
        rs = self.get_page_from_url(url=self.detect_url, data=data)
        # 转码 -- 二进制转成字典
        # rs = json.loads(rs)
        rs = rs.json()
        # 根据词语语言翻译词语
        # 设置翻译语言
        data['from'] = rs['lan']
        # 设置翻译后语言 -- 三目运算符
        data['to'] = 'en' if rs['lan'] == 'zh' else 'zh'
        # 发送翻译请求
        rs = self.get_page_from_url(self.trans_url, data)
        # 转码 请求响应
        rs = rs.json()
        # 输出翻译结果
        print(rs['trans'][0]['dst'])


if __name__ == '__main__':
    # 获取命令行上python 文件名  数据
    # print(sys.argv)
    word = sys.argv[1]
    # word = "你好"
    fy = FanYiSpider(word)
    fy.run()

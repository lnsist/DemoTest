"""
    使用代理池爬取 搜狗公众号, 反爬概率高
    使用Redis数据库构造一个爬取队列,
    将封装好的队列序列化后放入数据库, 等待调度,
    请求失败, 则重新放回队列, 等待下次调度,
    请求成功, 将数据存储到MySQL中,
    获取的数据是, 微信公众号的文章, 正文, 发表日期, 公众号等内容
date: 18-10-16 下午8:37
"""
import re

from requests import Request
import redis
from pickle import dumps, loads
from requests import Session
from urllib.parse import urlencode
from pyquery import PyQuery as pq
from requests import ReadTimeout
from requests import ConnectionError
from 数据库.MySQL业务类 import MySQL
import 爬虫.网络访问 as http_request

# 超时时长
TIME_OUT = 10
# 主机
REDIS_HOST = "localhost"
# 端口
REDIS_PORT = 6379
# 密码
REDIS_PASSWORD = "123456"
# 数据库key
REDIS_KEY = "proxies"
# 获取随机代理接口
PROXY_POOL_URL = "http://127.0.0.1:5000/random"
# 状态码 集合
VALID_STATUSES = [200, 304, 301, 302]

# 测试地址
BASE_URL = "https://weixin.sogou.com/weixin"
# 搜索关键字
KEYWORD = "人工智能"


class MySQLApp(MySQL):
    """
        继承父类, 自定义一个判断是否已爬取方法
    """

    def is_climb(self, url):
        """
            根据url请求路径, 判断是否已爬取
        :param url: 请求路径
        :return: 是否已爬取 -- 有数据则已爬取, 无数据则未爬取
        """
        # table 表名   condition 查询条件语句, 值要用''括起来表示字符串
        select_data = super().select_data(table="articles", condition="url='" + url + "'")
        # 返回是否已爬取
        return bool(select_data)


class WeixinRequest(Request):
    """
        自定义Request -- 自定义需要保留的属性
    """

    def __init__(self, url, callback, method="GET", headers=None, need_proxy=True, fail_time=0, timeout=TIME_OUT):
        """
            初始化, 自定义属性
        """
        # 调用父级初始化
        super(WeixinRequest, self).__init__()
        Request.__init__(self, method, url, headers)

        # 以下是自定义属性
        # 回调
        self.callback = callback
        # 需要更换代理
        self.need_proxy = need_proxy
        # 失败次数
        self.fail_time = fail_time
        # 超时时间
        self.timeout = timeout


class RedisQueue(object):
    """
        数据库操作 -- 队列
    """

    def __init__(self):
        """
            初始化数据库 -- db=13
        """
        self.db = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=13)

    def add(self, request):
        """
            向队列添加序列化后的Requset
        :param request: 请求对象
        :return: 添加结果
        """
        # 当前 requset 是WeixinRequest
        if isinstance(request, WeixinRequest):
            # 返回数据库添加结果, 数据库Key, 序列化后的request
            return self.db.rpush(REDIS_KEY, dumps(request))

    def pop(self):
        """
            取出下一个Request并反序列化
        :return: Request
        """
        # 列表不为空
        if self.db.llen(REDIS_KEY):
            # 返回第一个Request并反序列化
            return loads(self.db.lpop(REDIS_KEY))
        # 返回空
        return None

    def empty(self):
        """
            判断当前数据库是否为空
        :return: 是否为空
        """
        # 返回当前数据库是否为空
        return self.db.llen(REDIS_KEY) == 0


class Spider(object):
    """
        自定义WeixinRequest添加队列
    """
    # headers = {
    #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    #     "Accept-Encoding": "gzip, deflate",
    #     "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2,mt;q=0.2",
    #     "Cache-Control": "max-age=0",
    #     "Connection": "keep-alive",
    #     "Cookie": "CXID=BEE955374D8A8ADF86052E820E010E54; SUID=84C660705C68860A5BA75B79000826EE; "
    #               "SUV=1538915270616586; SMYUV=1538915270616333; UM_distinctid=1664e7f80b078e-028a6a1bcc183-3c7"
    #               "f0257-1fa400-1664e7f80b180b; ad=CMsn9kllll2bICHilllllVmDQ3kllllltpRpPlllll9llllljylll5@@@@@@@"
    #               "@@@; ABTEST=8|1539692981|v1; weixinIndexVisited=1; SNUID=5A11F5E59693EDC222048A8D96008CF4; IPL"
    #               "OC=CN4400; ppinf=5|1539950120|1541159720|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTozOm95M3"
    #               "xjcnQ6MTA6MTUzOTk1MDEyMHxyZWZuaWNrOjM6b3kzfHVzZXJpZDo0NDpvOXQybHVJMjlhLWVJR21wTFl3RTFOaW5BUC1NQH"
    #               "dlaXhpbi5zb2h1LmNvbXw; pprdig=B6tyhVpGoMOr__4IL3FLnrQWEyEhhnl9a4Lvxg0FgK1Zb4-7P4A4Fw3BAF6XqTvhHa6"
    #               "SUeBkZqHw9Ei66XLhFTUE_fzBDgq-B6qvxEDmfeXnk3KP_1pr8pRnlI7tMvD6SohbX7sJT8AdzMmbogSywXcXZA8IoaA3MK4Ld"
    #               "QhjFB0; sgid=23-35589827-AVvJxiajtfmuEg6WDXCLPTRw; ppmdig=1539950120000000ba077df50ac0e3fb111c05974"
    #               "25837ad; sct=5; JSESSIONID=aaaJuH8hLItda4v4GgIzw",
    #     "Host": "weixin.sogou.com",
    #     "Upgrade-Insecure-Requests": "1",
    #     "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
    # }

    # 请求头, 删除了 cookie 不登陆爬取信息
    headers = {
        # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        # "Accept-Encoding": "gzip, deflate",
        # "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4,zh-TW;q=0.2,mt;q=0.2",
        # "Cache-Control": "max-age=0",
        # "Connection": "keep-alive",
        # "Cookie": "pgv_pvid=8461201050; rewardsn=; wxtokenkey=777",
        # "Host": "weixin.sogou.com",
        # "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
    }
    # 会话
    session = Session()
    # 队列
    queue = RedisQueue()
    # 数据库
    mysql = MySQLApp(db="weixin_sogou")

    def start(self, base_url=BASE_URL, keyword=KEYWORD):
        """
            初始化, 向队列添加数据
        :return:
        """
        # 跟新请求头
        self.session.headers.update(Spider().headers)
        # 拼接请求头
        start_url = base_url + "?" + urlencode({"query": keyword, "type": 2})
        # 实例化 WexinRequest 添加至数据库队列中,
        weixin_request = WeixinRequest(url=start_url, callback=self.parse_index, need_proxy=True)
        # 添加队列
        self.queue.add(weixin_request)

    def request(self, weixin_request):
        """
            执行请求访问
        :param weixin_request: 请求
        :return: 响应
        """
        # 捕获异常
        try:
            # 代理字典
            proxies = {}
            # 是否需要换代理
            if weixin_request.need_proxy:
                # 获取请求访问响应 -- 获取代理
                proxy = http_request.get_page(PROXY_POOL_URL)
                # 获取成功
                if proxy:
                    # 输出提示
                    print("成功获取代理 " + proxy)
                    # 拼接代理
                    proxies = {
                        "http": "http://" + proxy,
                        "https": "https://" + proxy
                    }
            # 返回 请求访问响应报文 -- 会话发送 allow_redirects是否允许重定向
            return self.session.send(weixin_request.prepare(), timeout=weixin_request.timeout, allow_redirects=True, proxies=proxies)
        except (ConnectionError, ReadTimeout) as e:
            # 输出异常提示
            print(e)
            #
            return False

    def parse_index(self, response):
        """
            回调 -- 解析索引页, 生成新的列队消息
        :param response: 响应报文
        :return: 新的列队消息
        """
        # 解析响应
        doc = pq(response.text)
        # 解析内容 -- 获取页面列表信息
        items = doc(".news-box .news-list li .txt-box h3 a").items()
        # 循环 列表信息, 请求访问获取信息内容
        for item in items:
            # 获取 href 内容
            url = item.attr("href")
            # 如果已爬取过的网页, 直接进入下一次循环
            if Spider().mysql.is_climb(url):
                # 输出提示
                print("此请求访问, 已爬取, 执行下一条访问")
                # 执行下一次
                continue
            # 实例化队列, 设置 请求路径 指向回调 -- 解析报文
            weixin_request = WeixinRequest(url=url, callback=self.parse_detail)
            # 生成返回 队列信息
            yield weixin_request
        # id选择器 sogou_next, 获取 href 内容 -- 下一页
        next = doc("#sogou_next").attr("href")
        # 如果 下一页 存在
        if next:
            # 拼接请求路径
            url = BASE_URL + str(next)
            # 实例化队列, 设置 请求路径 指向回调 -- 解析索引页
            weixin_request = WeixinRequest(url=url, callback=self.parse_index, need_proxy=True)
            # 生成返回 队列信息
            yield weixin_request

    @staticmethod
    def parse_detail(response):
        """
            解析详情页
        :param response: 响应报文
        :return: 微信公众号文章
        """
        # 加载 响应报文
        doc = pq(response.text)
        # 创建 正则表达式, 并设置格式
        phone_num_re = re.compile(r"\d{4}-\d{2}-\d{2}")
        # 匹配响应报文
        date = phone_num_re.search(response.text).group(0)
        # 解析内容
        data = {
            "id": "0",
            "title": doc(".rich_media_title").text(),
            "content": doc(".rich_media_content").text(),
            "date": date,
            "nickname": doc("#js_profile_qrcode > div > strong").text(),
            "wechat": doc("#js_profile_qrcode > div > p:nth-child(3) > span").text()
        }
        # 返回内容 -- 微信公众号具体文章
        yield data

    def error(self, weixin_request):
        """
            错误处理
        :param weixin_request: 请求
        :return:
        """
        # 错误累计
        weixin_request.fail_time = weixin_request.fail_time + 1
        # 输出提示
        print("请求错误 ", weixin_request.fail_time, " 次数 ", weixin_request.url)
        # 错误次数小于 10
        if weixin_request.fail_time < 10:
            # 重新发送 列队消息
            self.queue.add(weixin_request)

    def schedule(self):
        """
            调度所有功能
        :return:
        """
        # 队列不为空
        while not self.queue.empty():
            # 获取第一个列队消息
            weixin_request = self.queue.pop()
            # 获取回调
            callback = weixin_request.callback
            # 输出提示
            print("准备请求访问 " + weixin_request.url)
            # 如果已爬取过的网页, 直接进入下一次循环
            if Spider().mysql.is_climb(weixin_request.url):
                # 输出提示
                print("此请求访问, 已爬取, 执行下一条访问")
                # 执行下一次
                continue
            # 请求访问
            response = self.request(weixin_request)
            # 响应报文不为空, 且状态码在集合中
            if response and response.status_code in VALID_STATUSES:
                # 回调方法传入响应报文, 获取返回值
                results = list(callback(response))
                # 如果不为空
                if results:
                    # 循环信息
                    for result in results:
                        # 输出提示
                        print("新队列信息 ", result)
                        # 判断是否自定义Request
                        if isinstance(result, WeixinRequest):
                            # 列队添加信息
                            self.queue.add(result)
                        # 如果是解析后的字典类型
                        if isinstance(result, dict):
                            # 添加当前页面请求路径, 用以判断是否已爬取, 去重
                            result["url"] = weixin_request.url
                            # 如果已爬取过的网页, 直接进入下一次循环
                            if Spider().mysql.is_climb(weixin_request.url):
                                # 输出提示
                                print("此请求访问, 已爬取, 执行下一条访问")
                                # 执行下一次
                                continue
                            # 插入数据库
                            Spider.mysql.insert_data("articles", result)
                else:
                    # 输出提示
                    print("回调结果为空")
                    # 回调报错
                    self.error(weixin_request)
            else:
                # 输出提示
                print("请求结果为空")
                # 请求访问报错
                self.error(weixin_request)

    def main(self):
        """
            主入口
        :return:
        """
        # 准备工作
        self.start()
        # 真正爬取
        self.schedule()


if __name__ == '__main__':
    # 调度
    spider = Spider()
    # 主入口
    spider.main()

"""
    批量爬去网络代理, 使用元类
date: 18-10-12 下午9:00
"""

from pyquery import PyQuery as pq
from 爬虫.代理.utils import get_page


class ProxyMetaclass(type):
    """
        网络代理爬取元类
    """

    def __new__(mcs, name, bases, attrs):
        # 爬取函数名的计数
        count = 0
        # 自定义属性 __CrawlFunc__ 存放的是各个具体爬取代理的函数名
        attrs["__CrawlFunc__"] = []
        # 循环传入的属性
        for k, v in attrs.items():
            # 如果属性的key包含 crawl_
            if "crawl_" in k:
                # 自定义属性添加此属性 -- 保存函数名
                attrs["__CrawlFunc__"].append(k)
                # 爬取函数名的计数累加
                count += 1
        # 自定义属性 __CrawlFuncCount__ 爬取函数名的总数
        attrs["__CrawlFuncCount__"] = count
        # 返回, 自定义后创建出来的类
        return type.__new__(mcs, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    """
        网络代理爬取器
    """

    def get_proxies(self, callback):
        """
            根据传入的函数名,
            使用eval变成表达式直接调用具体的函数,
            请求访问后返回网络代理
        :param callback: 函数名
        :return: 网络代理
        """
        # 代理列表
        proxies = []
        # 循环 self.函数() 获取代理 -- eval 去除""变成表达式
        for proxy in eval("self.{}()".format(callback)):
            # 输出提示
            print("成功获取到代理", proxy)
            # 代理列表添加代理
            proxies.append(proxy)
        # 返回代理列表
        return proxies

    @staticmethod
    def crawl_daili66(page_count=4):
        """
            获取代理66的代理
        :param page_count: 页码
        :return: json格式代理 -- 生成器
        """
        # 请求路径
        start_url = "http://www.66ip.cn/{}.html"
        # 列表生成式, 生成格式化路径, 传入页码 从1开始到page_count
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        # 循环访问路径
        for url in urls:
            # 输出提示
            print("正在爬取", url)
            # 请求访问
            html = get_page(url)
            # 响应报文不为空
            if html:
                # 加载源码
                doc = pq(html)
                # 解析源码, 选择器获取代理所在控件
                trs = doc(".containerbox table tr:gt(0)").items()
                # 循环控件
                for tr in trs:
                    # 获取代理ip
                    ip = tr.find("td:nth-child(1)").text()
                    # 获取代理端口
                    port = tr.find("td:nth-child(2)").text()
                    # 生成 json格式代理  ip:端口
                    yield ":".join([ip, port])

    @staticmethod
    def crawl_proxy360():
        """
            获取Proxy360的代理
        :return: json格式代理 -- 生成器
        """
        # 请求路径
        start_url = "http://www.proxy360.cn/Region/China"
        # 输出提示
        print("正在爬取", start_url)
        # 请求访问
        html = get_page(start_url)
        # 响应报文不为空
        if html:
            # 加载源码
            doc = pq(html)
            # 解析源码, 选择器获取代理控件
            lines = doc("div[name='list_proxy_ip']").items()
            # 循环控件
            for line in lines:
                # 获取代理ip
                ip = line.find(".tbBottomLine:nth-child(1)").text()
                # 获取代理端口
                proxy = line.find(".tbBottomLine:nth-child(2)").text()
                # 生成 json格式代理  ip:端口
                yield ":".join([ip, proxy])

    @staticmethod
    def crawl_goubanjia():
        """
            获取Goubanjia的代理
        :return: json格式代理 -- 生成器
        """
        # 请求路径
        start_url = "http://www.goubanjia.com/free/gngn/index.shtml"
        # 请求访问
        html = get_page(start_url)
        # 响应报文不为空
        if html:
            # 加载源码
            doc = pq(html)
            # 解析源码, 选择器获取代理控件
            tds = doc("td.ip").items()
            # 循环控件
            for td in tds:
                # 移除p标签
                td.find("p").remove()
                # 将代理控件" "替换成"", 生成 json格式代理  ip:端口
                yield td.text().replace(" ", "")


if __name__ == '__main__':
    # 创建网络代理爬取器
    poxy_crawler = Crawler()
    # 爬取器中的爬取函数集合
    print(poxy_crawler.__CrawlFunc__)
    # 循环爬取函数集合 -- funcName 爬取函数名
    for funcName in poxy_crawler.__CrawlFunc__:
        # 调用具体的爬取函数
        poxy_crawler.get_proxies(funcName)

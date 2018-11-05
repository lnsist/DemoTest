"""
    代理池4个模块: 存储模块, 获取模块, 检测模式, 接口模块
    存储模块: 使用Redis的有序集合, 用来做代理的去重和状态标识,
    获取模块: 定时从代理网站获取代理, 将获取的代理传递给存储模块进行存储
    检测模块: 定时通过存储模块获取所有代理, 并对代理进行检测, 根据不同的检测结果对代理设置不同的标识
    接口模块: 通过Web API提供服务接口, 接口通过连接数据库并通过Web形式返回可用的代理

    获取模块, 定义好一套自动化获取网络代理函数,
    最后Getter类, 在获取模块得到代理后, 保存到Redis中
date: 18-10-11 下午9:34
"""
from pyquery import PyQuery as pq
from 爬虫.网络访问 import get_page
from 爬虫.代理.代理池.代理池_存储模块 import RedisClient

# 页码
MAX_PAGE = 100


class ProxyMetaclass(type):
    """
        获取模块 -- 元类
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
        获取模块, 指定元类metaclass=ProxyMetaclass
    """

    def __init__(self):
        """
            初始化
        """
        # 页码
        self.page_count = MAX_PAGE

    def get_proxies(self, callback):
        """
            根据传入的函数名, 回调
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

    def crawl_daili66(self):
        """
            获取代理66的代理
        :return: json格式代理 -- 生成器
        """
        # 请求路径
        start_url = "http://www.66ip.cn/{}.html"
        # 列表生成式, 格式化生成路径, 传入页码 从1开始到page_count
        urls = [start_url.format(page) for page in range(1, self.page_count + 1)]
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

    def crawl_xicidaili(self):
        """
            获取西刺代理的代理
        :return: json格式代理 -- 生成器
        """
        # 请求路径
        start_utl = "http://www.xicidaili.com/nn/{}"
        # 列表生成式, 格式化生成路径, 传入页码 从1开始到page_count
        urls = [start_utl.format(page) for page in range(1, self.page_count + 1)]
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
                # 解析源码, 选择器获取代理控件
                lines = doc.find("table tr").items()
                # 循环控件
                for line in lines:
                    # 获取代理ip
                    ip = line.find("td:nth-child(2)").text()
                    # 获取代理端口
                    proxy = line.find("td:nth-child(3)").text()
                    # 生成 json格式代理  ip:端口
                    yield ":".join([ip, proxy])

    def crawl_kuaidaili(self):
        """
            获取快代理的代理
        :return: json格式代理 -- 生成器
        """
        # 请求路径
        start_utl = "https://www.kuaidaili.com/free/inha/{}/"
        # 列表生成式, 格式化生成路径, 传入页码 从1开始到page_count
        urls = [start_utl.format(page) for page in range(1, self.page_count + 1)]
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
                # 解析源码, 选择器获取代理控件
                lines = doc.find("table tbody tr").items()
                # 循环控件
                for line in lines:
                    # 获取代理ip
                    ip = line.find("td:nth-child(1)").text()
                    # 获取代理端口
                    proxy = line.find("td:nth-child(2)").text()
                    # 生成 json格式代理  ip:端口
                    yield ":".join([ip, proxy])

    def crawl_proxy360(self):
        """
            获取Proxy360的代理
        :return: json格式代理 -- 生成器
        """
        # 请求路径
        start_url = "http://www.swei360.com/free/?page={}"
        # 列表生成式, 格式化生成路径, 传入页码 从1开始到page_count
        urls = [start_url.format(page) for page in range(1, self.page_count + 1)]
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
                # 解析源码, 选择器获取代理控件
                lines = doc("table tbody tr").items()
                # 循环控件
                for line in lines:
                    # 获取代理ip
                    ip = line.find("td:nth-child(1)").text()
                    # 获取代理端口
                    proxy = line.find("td:nth-child(2)").text()
                    # 生成 json格式代理  ip:端口
                    yield ":".join([ip, proxy])

    @staticmethod
    # def crawl_goubanjia():
    def _goubanjia():
        """
            获取Goubanjia的代理 -- 收费了...
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


class Getter(object):
    """
        获取网络代理后, 保存到Redis中
    """

    def __init__(self):
        # redis数据库
        self.redis = RedisClient()
        # 网络代理获取器
        self.crawler = Crawler()

    def run(self):
        """
            执行获取网络代理后, 保存到Redis中
        :return:
        """
        # 输出提示
        print("获取器开始执行")
        # 循环获取器中的爬取函数名列表
        for callback_label in self.crawler.__CrawlFunc__:
            # 调用爬取函数, 获取网络代理
            proxies = self.crawler.get_proxies(callback_label)
            for proxy in proxies:
                # 保存网络代理
                self.redis.add(proxy)


if __name__ == '__main__':
    # 执行获取器
    Getter().run()

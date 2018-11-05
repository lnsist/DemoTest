"""
    通过mitmdump爬取, 得到APP中电子书信息
mitmdump可以很轻松的获取请求和响应信息, 但是手机的操作需要手动,
获取到的响应信息, 是最全面的, 不会由于手机未显示而未加载数据,

暂时没运行成功,,,  手机设置代理后, 无法上网
date: 18-10-26 下午4:05
"""
import pymongo
from mitmproxy import ctx
import json

# 数据库路径
MONGO_URL = "localhost"
# 数据库 -- 名称
MONGO_DB = "dedao"
# 数据库 -- 连接
MONGO_COLLECTION = "books"


def request(flow):
    """
        mitmproxy中请求处理的方法
    :param flow: HTTPFlow对象 -- 可获取请求信息
    :return:
    """
    # 获取请求信息
    f_request = flow.request
    # 获取日志打印指向, info级别
    info = ctx.log.info
    # 输出提示
    print("X".center(50, "X"))
    # 请求路径
    info(f_request.url)
    # 请求头
    info(str(f_request.headers))
    # cookies
    info(str(f_request.cookies))
    # 请求地址
    info(f_request.host)
    # 请求方法
    info(f_request.method)
    # 代理
    info(str(f_request.port))
    # 方案
    info(f_request.scheme)

    # 修改请求路径
    # f_request.url = "http://www.baidu.com"

def response(flow):
    """
        mitmproxy中响应处理的方法
    :param flow: HTTPFlow对象 -- 可获取响应信息
    :return:
    """
    # 数据库客户端
    client = pymongo.MongoClient(MONGO_URL)
    # 获取数据库
    db = client[MONGO_DB]
    # 获取数据库连接
    collection = db[MONGO_COLLECTION]
    # 电子书路径
    url = "https://dedao.igetget.com/v3/discover/bookList"
    # 如果当前请求路径是以 电子书路径开头
    if flow.request.url.startswith(url):
        # 获取响应体
        text = flow.response.text
        # json格式化
        data = json.loads(text)
        # 获取电子书列表信息
        books = data.get("c").get("list")
        # 循环
        for book in books:
            # 拼接当前电子书信息
            data = {
                "title": book.get("operating_title"),
                "cover": book.get("cover"),
                "summary": book.get("other_share_summary"),
                "price": book.get("price")
            }
            # 写日志
            ctx.log.info(str(data))
            # 存储到数据库
            collection.insert(data)



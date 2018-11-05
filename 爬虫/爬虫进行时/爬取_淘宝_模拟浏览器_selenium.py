"""使用selenium爬取淘宝商品 -- 保存在MongoBD中
淘宝 -- 整个页面都是通过Ajax获取的
date: 18-10-5 下午3:06
"""
from urllib.parse import quote

import pymongo
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pyquery import PyQuery as pq

# 火狐浏览器 -- 会弹出浏览器
# browser = webdriver.Firefox()

# PhantomJS  无界面浏览器
# browser = webdriver.PhantomJS()

# PhantomJS 缓存和禁用图片加载 选项  -- 提高效率
# SERVICE_ARGS = ("--load-images=false", "--disk-cache=true")

# 设置选项
# browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)

# 谷歌浏览器 -- 会弹出浏览器
browser = webdriver.Chrome()

# 谷歌浏览器选项
# chrome_options = webdriver.ChromeOptions()
# 添加选项 -- headless  无界面模式
# chrome_options.add_argument("--headless")
# 谷歌浏览器 -- 不会弹出浏览器, 无界面模式
# browser = webdriver.Chrome(chrome_options=chrome_options)

# 等待加载, 超时时间 10 秒 -- 指定等待条件, 如果匹配到即页面加载成功, 返回相应结果并向下执行, 否则 10 秒后抛出超时异常
wait = WebDriverWait(browser, 10)
# 搜索关键字
KEYWORD = "iPad"
# 数据库url
MONGO_URL = "localhost"
# 数据库
MONGO_DB = "taobao"
# 关键字
MONGO_COLLECTION = "products"
# 数据库客户端
client = pymongo.MongoClient(MONGO_URL)
# 淘宝数据库
db = client[MONGO_DB]


def index_page(page):
    """
        抓取索引页商品列表
    :param page: 页码
    :return:
    """
    # 标识抓取 页码
    print("正在抓取第", page, "页")
    try:
        # url拼接 -- quote转码 ( search_type=item 搜索类型, sort=sale-desc 销量搜索 )
        url = "https://s.taobao.com/search?q=" + quote(KEYWORD) + "&search_type=item&sort=sale-desc"
        # get访问
        browser.get(url)
        # 大于 1 页 -- 跳页操作
        if page > 1:
            # 页码输入框 -- presence_of_element_located 元素是否出现
            taobao_input = wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager div.form > input")))
            # 页码确定按钮 -- element_to_be_clickable 元素是否可点击
            taobao_submit = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "#mainsrp-pager div.form > span.btn.J_Submit")))
            # 清空页码
            taobao_input.clear()
            # 输入页码
            taobao_input.send_keys(page)
            # 点击页码确定按钮
            taobao_submit.click()

        # 等待页面加载完毕

        # 等待页面加载完毕, 可以搜索到此控件 -- text_to_be_present_in_element 某段文本是否出现在某元素中
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#mainsrp-pager li.item.active > span"), str(page)))
        # 等待页面加载完毕, 可以搜索到此控件 -- presence_of_element_located 元素是否出现
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".m-itemlist .items .item")))
        # 页面解析 -- 提取商品信息
        get_products()
    except TimeoutException:
        # 超时重新访问
        index_page(page)


def get_products():
    """
        提取商品信息
    :return:
    """
    # 获取源码
    html = browser.page_source
    # 构造 pq 解析对象
    doc = pq(html)
    # 获取商品列表 -- 迭代器
    items = doc("#mainsrp-itemlist .items .item").items()
    # 循环获取
    for item in items:
        # 商品字典拼接
        product = {
            # 图片
            "image": item.find(".pic .img").attr("data-src"),
            # 价格
            "price": item.find(".price").text(),
            # 成交量
            "deal": item.find(".deal-cnt").text(),
            # 标题
            "title": item.find(".title").text(),
            # 卖家店铺
            "shop": item.find(".shop").text(),
            # 店铺所在地
            "location": item.find(".location").text()
        }
        # 输出
        print(product)
        # 保存数据库
        save_to_mongo(product)


def save_to_mongo(result):
    """
        保存数据库 -- MongoDB
    :param result: 数据
    :return:
    """
    try:
        # 插入数据库
        if db[MONGO_COLLECTION].insert(result):
            # 成功提示
            print("存储到MongoDB成功")
    except Exception as e:
        print(e)
        print("存储到MongoDB失败")


# 最大页码
MAX_PAGE = 100
if __name__ == '__main__':
    # 循环获取商品
    for i in range(1, 2 + 1):
        index_page(i)

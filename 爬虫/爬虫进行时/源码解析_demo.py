"""各种解析方式

date: 18-9-28 下午6:56
"""
import re

from bs4 import BeautifulSoup
from lxml import etree
# from pyquery import PyQuery as pq


def pares_by_reex(html):
    """
        正则表达式解析
    由于需要拼写正则表达式, 麻烦, 复杂, 而且很容易出错
    以 dd 标签为一组, 分组匹配
    :param html: 源码
    :return: 生成器
    """
    # 表达式
    pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?'
                         'star.*?>(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>', re.S)
    # 匹配
    items = re.findall(pattern, html)

    # 循环解析封装信息
    for item in items:
        # 生成器 -- 封装成字典
        yield {
            # 排名
            "index": item[0],
            # 图片
            "image": item[1],
            # 电影名称
            "title": item[2].strip(),
            # 主演：张国荣,张丰毅,巩俐    --   从 主演: 后开始截取字段
            "actor": item[3].strip()[3:] if len(item[3].strip()) > 3 else "",
            # 上映时间：1993-01-01    --    从 上映时间: 后开始截取字段
            "time": item[4].strip()[5:] if len(item[4].strip()) > 5 else "",
            # 拼接评分
            "score": item[5].strip() + item[6].strip()
        }


def pares_bt_xpath_back(html):
    """通过XPath解析  '//' 全文检索, 每次都是从头到尾
    当前是一次性全部检索返回列表的标签, 不能顺序的一个一个的获取标签

    paers_html.xpath('//i[contains(@class, "board-index")]/text()')
    返回匹配成功的所有标签, 类型类似列表

    contains 函数用于匹配多个class属性获取其中一个
    :return:
    """
    # 解析 -- 文件
    paers_html = etree.HTML(html)
    # 解析源码 -- 转为二进制 -- 设置utf-8格式, 默认为空
    # paers_html = etree.parse("./猫眼电影Top100第一页.html", etree.HTMLParser(encoding="utf-8"))

    # 获取所有 排名 标签
    indexs = paers_html.xpath('//i[contains(@class, "board-index")]/text()')
    # 获取所有 图片 标签
    images = paers_html.xpath('//a[@class="image-link"]/img/@data-src')
    # 获取所有 电影名 标签
    titles = paers_html.xpath('//p[@class="name"]/a[@data-act="boarditem-click"]/text()')
    # 获取所有 主演 标签
    actors = paers_html.xpath('//p[@class="star"]/text()')
    # 获取所有 上映时间 标签
    times = paers_html.xpath('//p[@class="releasetime"]/text()')
    # 获取所有 评分整数 标签
    score_as = paers_html.xpath('//p[@class="score"]/i[@class="integer"]/text()')
    # 获取所有 评分小数 标签
    score_bs = paers_html.xpath('//p[@class="score"]/i[@class="fraction"]/text()')

    # 循环解析封装信息
    for i in range(10):
        # 生成器 -- 封装成字典
        yield {
            # 排名
            "index": indexs[i],
            # 图片
            "image": images[i],
            # 电影名称
            "title": titles[i].strip(),
            # 主演：张国荣,张丰毅,巩俐    --   从 主演: 后开始截取字段
            "actor": actors[i].strip()[3:] if len(actors[i].strip()) > 3 else "",
            # 上映时间：1993-01-01    --    从 上映时间: 后开始截取字段
            "time": times[i].strip()[5:] if len(times[i].strip()) > 5 else "",
            # 拼接评分
            "score": score_as[i].strip() + score_bs[i].strip()
        }


def pares_bt_xpath(html):
    """通过XPath解析  '//' 全文检索, 每次都是从头到尾  './/' 在当前标签内的全局检索
    paers_html.xpath('//i[contains(@class, "board-index")]/text()')
    返回匹配成功的所有标签, 类型类似列表

    当前为缩小范围, 不要每次都循环整个源码, 缩小到具体内容的父类中<dd>
    注意在以获取的范围中, 获取具体内容, 不要用//全局检索, 不然就很蠢 .//是在当前标签内的全局检索
    :return:
    """
    # 解析 -- 文件
    paers_html = etree.HTML(html)
    # 解析源码 -- 转为二进制 -- 设置utf-8格式, 默认为空
    # paers_html = etree.parse("./猫眼电影Top100第一页.html", etree.HTMLParser(encoding="utf-8"))
    # 获取范围 -- dd标签为一组
    dds = paers_html.xpath("//dd")

    # 循环解析封装信息
    for dd in dds:
        # 获取当前 排名 text
        # index = dd.xpath('.//i[contains(@class, "board-index")]/text()')[0]
        # 功能同上, 通过迭代器获取下一个数据
        index = dd.xpath('.//i[contains(@class, "board-index")]/text()').__iter__().__next__()
        # 获取当前 图片 属性data-src
        # image = dd.xpath('.//a[@class="image-link"]/img/@data-src')[0]
        # 功能同上, 通过迭代器获取下一个数据
        image = dd.xpath('.//a[@class="image-link"]/img/@data-src').__iter__().__next__()
        # 获取当前 电影名称 text
        # title = dd.xpath('.//p[@class="name"]/a[@data-act="boarditem-click"]/text()')[0].strip()
        # 功能同上, 通过迭代器获取下一个数据
        title = dd.xpath('.//p[@class="name"]/a[@data-act="boarditem-click"]/text()').__iter__().__next__().strip()
        # 获取当前 主演 text
        # actor = dd.xpath('.//p[@class="star"]/text()')[0].strip()
        # 功能同上, 通过迭代器获取下一个数据
        actor = dd.xpath('.//p[@class="star"]/text()').__iter__().__next__().strip()
        # 获取当前 上映时间 text
        # time = dd.xpath('.//p[@class="releasetime"]/text()')[0].strip()
        # 功能同上, 通过迭代器获取下一个数据
        time = dd.xpath('.//p[@class="releasetime"]/text()').__iter__().__next__().strip()
        # 获取当前 评分整数 text
        # socre_a = dd.xpath('.//p[@class="score"]/i[@class="integer"]/text()')[0].strip()
        # 功能同上, 通过迭代器获取下一个数据
        socre_a = dd.xpath('.//p[@class="score"]/i[@class="integer"]/text()').__iter__().__next__().strip()
        # 获取当前 评分小数 text
        # socre_b = dd.xpath('.//p[@class="score"]/i[@class="fraction"]/text()')[0].strip()
        # 功能同上, 通过迭代器获取下一个数据
        socre_b = dd.xpath('.//p[@class="score"]/i[@class="fraction"]/text()').__iter__().__next__().strip()
        # 生成器 -- 封装成字典
        yield {
            # 排名
            "index": index,
            # 图片
            "image": image,
            # 电影名称
            "title": title,
            # 主演：张国荣,张丰毅,巩俐    --   从 主演: 后开始截取字段
            "actor": actor[3:] if len(actor) > 3 else "",
            # 上映时间：1993-01-01    --    从 上映时间: 后开始截取字段
            "time": time[5:] if len(time) > 5 else "",
            # 拼接评分
            "score": socre_a + socre_b
        }


def pares_by_beutiful_soup_back(html):
    """Beautiful Soup 解析 -- 全文搜索, 很蠢
    soup.select(".board-index")
    返回匹配的所有标签, 类型类似列表

    当前每次匹配全文检索
    :param html: 源码
    :return:
    """
    # 解析 html 源码
    soup = BeautifulSoup(html, "lxml")

    # 获取所有 排名 标签
    indexs = soup.select(".board-index")
    # 获取所有 图片 标签
    images = soup.select(".board-img")
    # 获取所有 电影名 标签
    titles = soup.select("p.name a")
    # 获取所有 主演 标签
    actors = soup.select("p.star")
    # 获取所有 上映时间 标签
    times = soup.select("p.releasetime")
    # 获取所有 评分整数 标签
    score_as = soup.select("i.integer")
    # 获取所有 评分小数 标签
    score_bs = soup.select("i.fraction")

    # 循环解析封装信息
    for i in range(10):
        # 获取当前 排名 标签
        index = indexs[i].string
        # 获取当前 图片 属性 data-src
        image = images[i]["data-src"]
        # 获取当前 电影名称 标签
        title = titles[i].string.strip()
        # 获取当前 主演 标签
        actor = actors[i].string.strip()
        # 获取当前 上映时间 标签
        time = times[i].string.strip()
        # 获取当前 评分整数 标签
        score_a = score_as[i].string.strip()
        # 获取当前 评分小数 标签
        score_b = score_bs[i].string.strip()
        # 生成器 -- 封装成字典
        yield {
            # 排名
            "index": index,
            # 图片
            "image": image,
            # 电影名称
            "title": title,
            # 主演：张国荣,张丰毅,巩俐    --   从 主演: 后开始截取字段
            "actor": actor[3:] if len(actor) > 3 else "",
            # 上映时间：1993-01-01    --    从 上映时间: 后开始截取字段
            "time": time[5:] if len(time) > 5 else "",
            # 拼接评分
            "score": score_a + score_b
        }


def pares_by_beutiful_soup(html):
    """Beautiful Soup 解析
    soup.select(".board-index")
    返回匹配的所有标签, 类型类似列表

    当前为缩小范围检索, 不要每次都循环整个源码, 缩小到具体内容的父类中<dd>
    :param html: 源码
    :return:
    """
    # 解析 html 源码
    soup = BeautifulSoup(html, "lxml")
    # 获取范围 -- dd标签为一组
    dds = soup.select("dd")

    # 循环范围取出具体内容
    for dd in dds:
        # 获取当前 排名 文本
        index = dd.select(".board-index")[0].string
        # 获取当前 图片 属性 data-src
        image = dd.select(".board-img")[0]["data-src"]
        # 获取当前 电影名 文本
        title = dd.select("p.name a")[0].string.strip()
        # 获取当前 主演 文本
        actor = dd.select("p.star")[0].string.strip()
        # 获取当前 上映时间 文本
        time = dd.select("p.releasetime")[0].string.strip()
        # 获取当前 评分A 文本
        score_a = dd.select("i.integer")[0].string.strip()
        # 获取当前 评分B 文本
        score_b = dd.select("i.fraction")[0].string.strip()
        # 生成器 -- 封装成字典
        yield {
            # 排名
            "index": index,
            # 图片
            "image": image,
            # 电影名称
            "title": title,
            # 主演：张国荣,张丰毅,巩俐    --   从 主演: 后开始截取字段
            "actor": actor[3:] if len(actor) > 3 else "",
            # 上映时间：1993-01-01    --    从 上映时间: 后开始截取字段
            "time": time[5:] if len(time) > 5 else "",
            # 拼接评分
            "score": score_a + score_b
        }


def pares_by_pyquery_back(html):
    """通过pyquery解析
    doc(".board-index")
    返回的是一个类似列表的标签数据

    doc(".board-index").text()
    返回的是所有标签的text组合成以 " "空格为间隔的字符串, 遍历时自行切割成列表, 或者直接使用生成迭代器方法.items()

    类型类似列表的标签属性获取, 只能获取第一个匹配的, 所以需要循环, pyquery不可以直接循环获取到的标签, 需要在匹配信息时, 返回迭代器才可以循环
    当前为全文检索
    :return:
    """
    # 解析 html -- url
    # doc = pq(url="http://maoyan.com/board/4")
    # 解析 html -- 文件
    # doc = pq(filename="猫眼电影Top100第一页.html")
    # 解析 html -- 源码
    doc = pq(html)

    # 获取所有 排名 文本 以 " "空格为间隔的字符串
    indexs = doc(".board-index").text()
    # 获取所有 图片 文本 以 " "空格为间隔的字符串
    images = doc(".board-img").items()
    # 获取所有 电影名 文本 以 " "空格为间隔的字符串
    titles = doc("p.name a").text().strip()
    # 获取所有 主演 文本 以 " "空格为间隔的字符串
    actors = doc("p.star").text().strip()
    # 获取所有 上映时间 文本 以 " "空格为间隔的字符串
    times = doc("p.releasetime").text().strip()
    # 获取所有 评分整数 文本 以 " "空格为间隔的字符串
    score_as = doc("i.integer").text().strip()
    # 获取所有 评分小数 文本 以 " "空格为间隔的字符串
    score_bs = doc("i.fraction").text().strip()

    # 循环封装信息
    for i in range(10):
        # 排名
        index = indexs.split(" ")[i]
        # 图片
        image = images.__next__().attr("data-src")
        # 电影名
        title = titles.split(" ")[i]
        # 主演
        actor = actors.split(" ")[i]
        # 上映时间
        time = times.split(" ")[i]
        # 评分整数
        score_a = score_as.split(" ")[i]
        # 评分小数
        score_b = score_bs.split(" ")[i]
        yield {
            # 排名
            "index": index,
            # 图片
            "image": image,
            # 电影名称
            "title": title,
            # 主演：张国荣,张丰毅,巩俐    --   从 主演: 后开始截取字段
            "actor": actor[3:] if len(actor) > 3 else "",
            # 上映时间：1993-01-01    --    从 上映时间: 后开始截取字段
            "time": time[5:] if len(time) > 5 else "",
            # 拼接评分
            "score": score_a + score_b
        }


def pares_by_pyquery(html):
    """通过pyquery解析
    doc(".board-index")
    返回的是一个类似列表的标签数据

    doc(".board-index").text()
    返回的是所有标签的text组合成以 " "空格为间隔的字符串, 遍历时自行切割成列表, 或者直接使用生成迭代器方法.items()

    类型类似列表的标签属性获取, 只能获取第一个匹配的, 所以需要循环, pyquery不可以直接循环获取到的标签, 需要在匹配信息时, 返回迭代器才可以循环
    当前为缩小范围, 在范围内检索, 所以属性的获取可以直接获取当前标签即可
    :return:
    """

    # 解析 html -- url
    # doc = pq(url="http://maoyan.com/board/4")
    # 解析 html -- 文件
    # doc = pq(filename="猫眼电影Top100第一页.html")
    # 解析 html -- 源码
    doc = pq(html)

    # 获取范围 -- dd标签为一组
    dds = doc("dd").items()

    # 循环范围取出具体内容
    for dd in dds:
        # 获取当前 排名 文本
        index = dd(".board-index").text()
        # 获取当前 图片 文本
        image = dd(".board-img").attr("data-src")
        # 获取当前 电影名 文本
        title = dd("p.name a").text().strip()
        # 获取当前 主演 文本
        actor = dd("p.star").text().strip()
        # 获取当前 上映时间 文本
        time = dd("p.releasetime").text().strip()
        # 获取当前 评分整数 文本
        score_a = dd("i.integer").text().strip()
        # 获取当前 评分小数 文本
        score_b = dd("i.fraction").text().strip()
        # 生成器 -- 封装成字典
        yield {
            # 排名
            "index": index,
            # 图片
            "image": image,
            # 电影名称
            "title": title,
            # 主演：张国荣,张丰毅,巩俐    --   从 主演: 后开始截取字段
            "actor": actor[3:] if len(actor) > 3 else "",
            # 上映时间：1993-01-01    --    从 上映时间: 后开始截取字段
            "time": time[5:] if len(time) > 5 else "",
            # 拼接评分
            "score": score_a + score_b
        }


def main(html):
    """各种解析方式
    :param html: 源码
    :return:
    """
    # 正则表达式
    # for item in pares_by_reex(html):
    #     print(item)

    # XPath 解析 -- 很蠢的全文搜索
    # for item in pares_bt_xpath_back(html):
    #     print(item)

    # XPath 解析 -- 范围搜索
    for item in pares_bt_xpath(html):
        print(item)

    # Beautiful Soup 解析 -- 很蠢的全文搜索
    # for item in pares_by_beutiful_soup_back(html):
    #     print(item)

    # Beautiful Soup 解析 -- 范围搜索
    # for item in pares_by_beutiful_soup(html):
    #     print(item)

    # pyquery 解析 -- 很蠢的全文搜索
    # for item in pares_by_pyquery_back(html):
    #     print(item)

    # pyquery 解析 -- 范围搜索
    # for item in pares_by_pyquery(html):
    #     print(item)


if __name__ == '__main__':
    # 打开源码文件
    with open("猫眼电影Top100第一页.html", "r", encoding="utf-8") as f:
        # 入口方法
        main(f.read())

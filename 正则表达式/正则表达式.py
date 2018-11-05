"""
    正则表达式
        1, 向 re.compile()传入一个字符串值，表示正则表达式，它将返回一个 Regex 模式对象（或者就简称为 Regex 对象）
        2, Regex 对象的 search()方法查找传入的字符串， 寻找该正则表达式的所有匹配。
        如果字符串中没有找到该正则表达式模式， search()方法将返回 None。
        如果找到了该模式，search()方法将返回一个 Match 对象。
        Match 对象有一个 group()方法，它返回被查找字符串中实际匹配的文本。

        search()将返回一个 Match对象， 包含被查找字符串中的“ 第一次” 匹配的文本，
        而 findall()方法将返回一组字符串， 包含被查找字符串中的所有匹配。
"""
import re

# 创建 正则表达式, 并设置格式
phone_num_re = re.compile(r"\d{3}-\d{3}-\d{4}")
# 传入字符串, 或者匹配的数据, 没有匹配则返回none
mo = phone_num_re.search('我的电话号码 415-555-4242.')
# 匹配则返回数据, 否则none
print('找到手机号码: ' + mo.group())

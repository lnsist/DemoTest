"""有道翻译
写一个有道翻译的爬虫, 实现对输入的内容进行翻译
网址: http://fanyi.youdao.com/

@Date    : 2019-01-27 20:23
@Author  : lnsist
"""
import requests
import time
import random
import hashlib
from jsonpath import jsonpath

# 翻译URL
url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
# 翻译请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'Referer': 'http://fanyi.youdao.com/?keyfrom=dict2.top',
    'Cookie': 'OUTFOX_SEARCH_USER_ID=1562131724@157.122.54.188; JSESSIONID=abcg8FMrrOldA-2O6cQCw; _ntes_nnid=16715a627437993218510de79f7721a4,1542598664906; OUTFOX_SEARCH_USER_ID_NCOO=1826678448.2544272; DICT_LOGIN=8||1542599285861; DICT_FORCE=true; DICT_UGC=be3af0da19b5c5e6aa4e17bd8d90b28a|; ___rl__test__cookies=1542599556868'
}

# 录入要翻译的内容
word = input("请输入要查询的单词: ")

# 通过python模拟, js生成的可变参数

#           毫秒                  1-10的随机数
#       js中 new Date().getTime() 单位是毫秒, 是一个整数
#       python中time.time() 单位是秒, 是一个小数, * 1000 转换为s, 取整.
salt = int(time.time() * 1000) + random.uniform(1, 10)
# 获取要加密的字符串
sign = "fanyideskweb" + word + str(salt) + "sr_3(QOHT)L2dx#uuGR@r"

# 使用md5加密
sign = hashlib.md5(sign.encode()).hexdigest()

# 翻译请求的数据
data = {
    'i': word,
    'from': 'AUTO',
    'to': 'AUTO',
    'smartresult': 'dict',
    'client': 'fanyideskweb',
    'salt': salt,
    'sign': sign,
    'doctype': 'json',
    'version': '2.1',
    'keyfrom': 'fanyi.web',
    'action': 'FY_BY_CLICKBUTTION',
    'typoResult': 'false',
}
# 发送请求, 获取响应
response = requests.post(url, data=data, headers=headers)
# 提取翻译结果
result = jsonpath(response.json(), '$..tgt')[0]
print(result)
